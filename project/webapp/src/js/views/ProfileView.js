import { View } from 'backbone.marionette';
import baseTemplate from 'Templates/layouts/profile.html';
import profileSettingsTemplate from 'Templates/components/Profile/settings_tab.html';
import sidebarTemplate from 'Templates/components/Profile/sidebar.html';
import { Accounts, Threads, Civis } from '../collections';

import TabView from '../components/Profile/Tab';
import ProfileCivi from '../components/Profile/Civi';
import ProfileIssue from '../components/Profile/Issue';
import AccountChip from '../components/Account/Chip';
import Representative from '../components/Profile/Representative';

import 'Styles/account.less';

const ProfileView = View.extend({
  template: baseTemplate,

  regions: {
    civis: '#civis',
    followers: '#followers',
    following: '#following',
    issues: '#issues',
    myreps: '#myreps',
    settings: '#settings',
  },
  ui: {
    tabs: '.tabs',
  },

  templateContext() {
    return {
      currentUser: this.getOption('context').username,
      username: this.model.get('username'),
    };
  },

  initialize() {
    this.currentUser = this.getOption('context').username;
    this.username = this.model.get('username');
    this.isSave = false;

    this.listenTo(this.model, 'sync', this.postSync);

    return this;
  },

  postSync() {
    // Handle Data
    const civis = [];
    _.each(this.model.get('history'), (civiData) => {
      civis.push(JSON.parse(civiData));
    });
    this.model.set('civis', civis);

    this.tabTemplateContext = this.model.toJSON();
    this.tabTemplateContext.currentUser = this.currentUser;

    document.title = `${this.model.get('first_name')} ${this.model.get(
      'last_name',
    )} (@${this.model.get('username')})`;

    // M.Pushpin.init(this.$el.find('.account-settings'));
    this.renderView();
    this.postRender();

    if (_.find(this.model.get('followers'), follower => follower.username === this.currentUser)) {
      const followButton = this.$('#sidebar-follow-btn');
      followButton.addClass('btn-secondary');
      followButton.data('follow-state', true);
      followButton.html('');
    }
  },

  renderView() {
    if (this.isSave) {
      this.postRender();
    } else {
      $('.account-tabs .tab').on('dragstart', () => false);
      // this.$el.find('.account-settings').pushpin({ top: $('.account-settings').offset().top });
      this.$el.find('.scroll-col').height($(window).height());
    }
  },

  tabsRender() {
    this.showChildView(
      'civis',
      new TabView({
        collection: new Civis(this.model.get('civis')),
        collectionChildView: ProfileCivi,
        title: 'My Civi Activity',
      }),
    );
    this.showChildView(
      'followers',
      new TabView({
        collection: new Accounts(this.model.get('followers')),
        collectionChildView: AccountChip,
        title: `${this.model.get('followers').length} Followers`,
      }),
    );
    this.showChildView(
      'following',
      new TabView({
        collection: new Accounts(this.model.get('following')),
        collectionChildView: AccountChip,
        title: `${this.model.get('following').length} Following`,
      }),
    );
    this.showChildView(
      'issues',
      new TabView({
        collection: new Threads(this.model.get('issues')),
        collectionChildView: ProfileIssue,
        title: 'My Issues',
      }),
    );
    this.showChildView(
      'myreps',
      new TabView({
        collection: new Accounts(this.model.get('myreps')),
        collectionChildView: Representative,
        title: 'My Representatives',
      }),
    );

    if (this.username === this.currentUser) {
      this.showChildView('settings', profileSettingsTemplate(this.tabTemplateContext));
    }
  },
  postRender() {
    // Timestamp the image with a cachebreaker so that proper refersh occurs
    this.model.set({ profile_image: `${this.model.get('profile_image')}?${new Date().getTime()}` });
    this.$el
      .find('.account-settings')
      .empty()
      .append(sidebarTemplate(this.tabTemplateContext));
    this.tabsRender();
    this.isSave = false;

    M.Tabs.init(this.getUI('tabs'));
    M.updateTextFields();
  },

  events: {
    'click .follow-btn': 'followRequest',
    'submit #profile_image_form': 'handleFiles',
    'blur .save-account': 'saveAccount',
    'click .toggle-solutions': 'toggleSolutions',
    'change .profile-image-pick': 'previewImage',
    'keypress .save-account': 'checkForEnter',
  },

  toggleSolutions(event) {
    const id = $(event.currentTarget).data('id');
    const textElement = $(event.currentTarget).find('.button-text');
    const newText = textElement.text() === 'Show Solutions' ? 'Hide Solutions' : 'Show Solutions';
    textElement.text(newText);
    this.$(`#solutions-${id}`).toggleClass('hide');
  },

  previewImage() {
    const view = this;
    const img = this.$el.find('#id_profile_image');
    if (img.val()) {
      const uploadedImage = img[0].files[0];
      if (uploadedImage) {
        // const formData = new FormData(this.$el.find('#profile_image_form')[0]);
        const reader = new FileReader();

        reader.onload = (readerEvent) => {
          const previewImage = view.$el.find('.preview-image');
          previewImage.attr('src', readerEvent.target.result);

          view.toggleImgButtons();
        };
        reader.readAsDataURL(uploadedImage);
      }
    }
  },

  checkForEnter: (event) => {
    if (event.which === 13 && !event.shiftKey) {
      event.preventDefault();
      $(event.target).blur();
    }
  },

  toggleImgButtons() {
    this.$('.profile-image-pick').toggleClass('hide');
    this.$('.upload-image').toggleClass('hide');
    this.$('#confirmation-prompt').toggleClass('hide');
  },

  followRequest(event) {
    const apiData = {};
    const view = this;
    const followState = view.$(event.currentTarget).data('follow-state');
    const target = view.$(event.target);

    apiData.target = view.$(event.currentTarget).data('username');

    if (!followState) {
      $.ajax({
        url: '/api/follow/',
        type: 'POST',
        data: apiData,
        success() {
          M.toast({ html: `You are now following user ${apiData.target}` });
          target.addClass('btn-secondary');
          target.data('follow-state', true);
          target.html('');
        },
        error() {
          M.toast({ html: `Could not follow user ${apiData.target}` });
        },
      });
    } else {
      $.ajax({
        url: '/api/unfollow/',
        type: 'POST',
        data: apiData,
        success() {
          M.toast({ html: `You have unfollowed user ${apiData.target}` });
          target.removeClass('btn-secondary');
          target.html('FOLLOW');
          target.data('follow-state', false);
        },
        error() {
          M.toast({ html: `Could not unfollow user ${apiData.target}` });
        },
      });
    }
  },

  saveAccount(event) {
    const $this = $(event.target);
    const changeKey = $this.attr('id');
    const changeVal = $this.val().trim();
    const apiData = {};
    const view = this;

    if (view.model.get([changeKey]) === changeVal) {
      return;
    }

    apiData[changeKey] = changeVal;

    $.ajax({
      url: '/api/edituser/',
      type: 'POST',
      data: apiData,
      success() {
        M.toast({ html: 'Saved!' });

        view.isSave = true;
        view.model.fetch();
      },
    });
  },

  handleFiles(event) {
    event.preventDefault();
    const view = this;
    const formData = new FormData($('#profile_image_form')[0]);

    $.ajax({
      url: '/api/upload_profile/',
      type: 'POST',
      data: formData,
      cache: false,
      contentType: false,
      processData: false,
      success() {
        M.toast('Saved!', 5000);

        view.isSave = true;
        view.model.fetch();
      },
      error(data) {
        if (data.status === 400) {
          M.toast({ html: data.responseJSON.message, classes: 'red' });
        } else if (data.status === 500) {
          M.toast({ html: 'Internal Server Error', classes: 'red' });
        } else {
          M.toast({ html: data.statusText, classes: 'red' });
        }
      },
    });
    view.toggleImgButtons();

    return false;
  },
});

export default ProfileView;

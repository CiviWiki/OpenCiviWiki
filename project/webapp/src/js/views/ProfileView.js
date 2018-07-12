import { View } from 'backbone.marionette';

import baseTemplate from 'Templates/layouts/profile.html';
import followersTemplate from 'Templates/components/Profile/followers_tab.html';
import followingTemplate from 'Templates/components/Profile/following_tab.html';
import civisTemplate from 'Templates/components/Profile/my_civis_tab.html';
import issuesTemplate from 'Templates/components/Profile/my_issues_tab.html';
import profileSettingsTemplate from 'Templates/components/Profile/settings_tab.html';
import sidebarTemplate from 'Templates/components/Profile/sidebar.html';
import userCardTemplate from 'Templates/components/Account/card.html';

import 'Styles/account.less';

const ProfileView = View.extend({
  //   el: '#account',
  template: baseTemplate,

  templateContext() {
    return {
      currentUser: this.currentUser,
    };
  },

  initialize() {
    this.currentUser = this.getOption('username');
    this.isSave = false;
  },

  onRender() {
    document.title = `${this.model.get('first_name')} ${this.model.get('last_name')}`;

    $('.account-tabs .tab').on('dragstart', () => false);
    this.$el.find('.account-settings').pushpin({ top: $('.account-settings').offset().top });
    this.$el.find('.scroll-col').height($(window).height());
    this.postRender();

    if (_.find(this.model.get('followers'), follower => follower.username === this.currentUser)) {
      const followButton = this.$('#sidebar-follow-btn');
      followButton.addClass('btn-secondary');
      followButton.data('follow-state', true);
      followButton.html('');
    }
  },

  tabsRender() {
    this.$('#civis')
      .empty()
      .append(civisTemplate);
    this.$('#followers')
      .empty()
      .append(followersTemplate);
    this.$('#following')
      .empty()
      .append(followingTemplate);
    this.$('#issues')
      .empty()
      .append(issuesTemplate);
    this.$('#mybills')
      .empty()
      .append(this.mybillsTemplate());
    const settingsEl = this.$('#settings');
    if (settingsEl.length) {
      settingsEl.empty().append(profileSettingsTemplate);
      M.updateTextFields();
    }
  },

  postRender() {
    // Timestamp the image with a cachebreaker so that proper refersh occurs
    this.model.set({ profile_image: `${this.model.get('profile_image')}?${new Date().getTime()}` });
    this.$el
      .find('.account-settings')
      .empty()
      .append(sidebarTemplate);
    this.tabsRender();
    M.AutoInit();
    this.isSave = false;
  },

  events: {
    'click .follow-btn': 'followRequest',
    'submit #profile_image_form': 'handleFiles',
    'blur .save-account': 'saveAccount',
    'mouseenter .user-chip-contents': 'showUserCard',
    'mouseleave .user-chip-contents': 'hideUserCard',
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

  showUserCard(event) {
    const view = this;
    const { username } = event.currentTarget.dataset;
    if (!$(`#usercard-${username}`).hasClass('open')) {
      clearTimeout(this.showTimeout);
      this.showTimeout = setTimeout(() => {
        $.ajax({
          type: 'POST',
          url: `/api/account_card/${username}`,
          success(data) {
            const cardData = data;
            cardData.isCurrentUser = false;
            if (this.currentUser === data.username) {
              cardData.isCurrentUser = true;
            }
            view
              .$(event.currentTarget)
              .parent()
              .after(userCardTemplate(cardData));
            // Hover Elements
            const target = view.$(event.currentTarget);

            const targetCard = view.$(`#usercard-${username}`);

            targetCard
              .stop()
              .fadeIn('fast', () => {
                // Positions
                const pos = target.offset();

                // Dimenions
                const cardHeight = targetCard.height();
                const chipHeight = target.height();
                const documentHeight = $(window).height();
                const scroll = view.$('.scroll-col').scrollTop();

                let top;
                if (
                  target[0].getBoundingClientRect().top + cardHeight + chipHeight
                  >= documentHeight
                ) {
                  top = pos.top + scroll - cardHeight - chipHeight - 2;
                } else {
                  top = pos.top + scroll + 25;
                }
                const left = target.position().left + 20;

                // Determine placement of the hovercard
                targetCard.css({
                  top,
                  left,
                });
              })
              .addClass('open');
          },
          error() {
            // No card for you!
          },
        });
      }, 200);
    }
  },

  hideUserCard(event) {
    const view = this;
    const { username } = event.currentTarget.dataset;
    const card = view.$('.user-card');
    if (`timeout-${username}` in view) {
      clearTimeout(view[`timeout-${username}`]);
    }
    clearTimeout(view.showTimeout);
    view[`timeout-${username}`] = setTimeout(() => {
      card.fadeOut('fast', () => {
        $(view).remove();
      });
    }, 200);
    $(`#usercard-${username}`).hover(
      () => {
        if (`timeout-${username}` in view) {
          clearTimeout(view[`timeout-${username}`]);
        }
      },
      () => {
        if (`timeout-${username}` in view) {
          clearTimeout(view[`timeout-${username}`]);
        }
        view[`timeout-${username}`] = setTimeout(() => {
          card.fadeOut('fast', () => {
            $(view).remove();
          });
        }, 100);
      },
    );
  },

  // showRawRatings(event) {
  //   $(event.target)
  //     .closest('.rating')
  //     .find('.rating-score')
  //     .toggleClass('hide');
  //   $(event.target)
  //     .closest('.rating')
  //     .find('.rating-percent')
  //     .toggleClass('hide');
  // },

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

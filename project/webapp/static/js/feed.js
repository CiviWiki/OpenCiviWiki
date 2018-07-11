cw = cw || {};

cw.FeedThreadModel = BB.Model.extend({
  defaults: {
    thread: {
      id: 'No Type',
      title: 'Civi Title',
      summary: 'Thread Summary',
      created: 'No Date',
      category_id: 20, // ID for "Other"
      image: 'static/img/no_image_md.png',
    },
    author: {
      username: 'None',
      full_name: 'No Name',
      profile_image: 'static/img/no_image_md.png',
    },
    stats: {
      num_views: 0,
      num_civis: 0,
      num_solutions: 0,
    },
  },
});

cw.FeedThreadCollection = BB.Collection.extend({
  model: cw.FeedThreadModel,

  url() {
    return '/api/feed/';
  },

  filterCategory(category_id) {
    const filtered = this.models.filter(
      thread_data => thread_data.get('thread').category_id === category_id,
    );
    return filtered;
  },
});

cw.FeedView = BB.View.extend({
  el: '#feed',
  template: _.template($('#feed-template').html()),
  feedListTemplate: _.template($('#feed-list-template').html()),

  initialize(options) {
    const _this = this;
    this.options = options || {};
    this.categories = this.options.categories;
    this.threads = this.options.threads.toJSON();
    this.draft_threads = this.options.draft_threads.toJSON();
    this.render();

    this.options.threads.on('sync', () => {
      _this.threads = _this.options.threads.toJSON();
      _this.render();
    });
  },

  render() {
    const user_categories = this.options.user_categories;
    const filtered_categories = _.filter(
      this.options.categories,
      c => _.contains(user_categories, c.id),
      user_categories,
    );

    const template_var = {
      trending: this.options.trending,
      draft_threads: this.draft_threads,
      categories: this.options.categories,
      user_categories: filtered_categories,
    };
    this.$el.empty().append(this.template(template_var));

    this.renderNav();
    this.renderModals();
    this.renderFeedList();
  },

  renderNav() {
    this.updatePriorityNav();
    $(window).on('resize', this.updatePriorityNav.bind(this));
  },

  renderModals() {
    this.newThreadView = new cw.NewThreadView({
      info: this.options,
    });

    this.CategoriesView = new cw.CategoriesView({
      categories: this.options.categories,
      user_categories: this.options.user_categories,
      mainView: this,
    });
  },

  renderFeedList() {
    const template_var = {
      categories: this.options.categories,
      threads: this.threads,
    };
    this.$('#feed-list')
      .empty()
      .append(this.feedListTemplate(template_var));
    this.$('.scroll-col').height($(window).height() - this.$('nav').height());
  },

  setUserCategories(new_list) {
    this.options.user_categories = new_list;
    return this;
  },

  updatePriorityNav() {
    const dropdown = this.$('#categories-dropdown');
    let navWidth = this.$('#user-categories-list > li.dropdown-wrapper').width()
      + this.$('#user-categories-list > li.category-all').width();
    const containerWidth = this.$('.nav-categories').width();

    this.$('#user-categories-list > li.user-categories').each(function () {
      navWidth += $(this).width();
    });

    if (navWidth > containerWidth) {
      const lastItem = this.$('#user-categories-list > li.user-categories').last();
      if (lastItem.text()) {
        lastItem.attr('data-width', lastItem.width());
        dropdown.prepend(lastItem);
        this.updatePriorityNav();
      }
    } else {
      const firstDropdownElement = dropdown.children().first();
      if (navWidth + firstDropdownElement.data('width') < containerWidth) {
        firstDropdownElement.insertBefore(this.$('#user-categories-list > li.dropdown-wrapper'));
      }
    }
  },

  events: {
    'click .new-thread': 'openNewThreadModal',
    'click .category-button': 'openCategoryModal',
    'click .category-item': 'filterFeed',
  },

  filterFeed(e) {
    const target = $(e.target);
    const selectedCategory = target.data('id');
    if (selectedCategory === 'arrow') {
    } else {
      if (selectedCategory === 'all') {
        this.threads = this.options.threads.toJSON();
      } else if (_.contains(this.options.user_categories, selectedCategory)) {
        this.threads = JSON.parse(
          JSON.stringify(this.options.threads.filterCategory(selectedCategory)),
        );
      }
      this.renderFeedList();
      this.$('.category-item').removeClass('active');
      target.addClass('active');
    }
  },

  allFeed() {
    this.$('.category-item').removeClass('active');
    this.$('.category-all > .category-item').addClass('active');
  },

  openNewThreadModal() {
    this.newThreadView.show();
  },
  openCategoryModal() {
    this.CategoriesView.show();
  },
});

cw.NewThreadView = BB.View.extend({
  el: '.new-thread-modal-holder',
  template: _.template($('#new-thread-template').html()),

  initialize(options) {
    this.options = options.info;
    this.imageMode = '';
    this.render();
  },

  render() {
    this.$el.empty().append(this.template());
    cw.materializeShit();
  },

  show() {
    this.$('.new-thread-modal').openModal();
  },

  hide() {
    this.$('.new-thread-modal').closeModal();
  },

  events: {
    'click .cancel-new-thread': 'cancelThread',
    'click .create-new-thread': 'createThread',
    'click .draft-new-thread': 'draftThread',
    'click #image-from-computer': 'showImageUploadForm',
    'click #image-from-link': 'showImageLinkForm',
    'change #thread-location': 'showStates',
  },

  cancelThread() {
    this.hide();
  },
  showImageUploadForm() {
    this.imageMode = 'upload';
    this.$('#attachment_image_form').removeClass('hide');
    this.$('#link-image-form').addClass('hide');
  },
  showImageLinkForm() {
    this.imageMode = 'link';
    this.$('#attachment_image_form').addClass('hide');
    this.$('#link-image-form').removeClass('hide');
  },
  showStates() {
    const level = this.$el.find('#thread-location').val();
    if (level === 'state') {
      this.$('.new-thread-state-selection').removeClass('hide');
    } else {
      this.$('.new-thread-state-selection').addClass('hide');
    }
  },

  createThread() {
    const _this = this;

    const title = this.$el.find('#thread-title').val();

    const summary = this.$el.find('#thread-body').val();

    const level = this.$el.find('#thread-location').val();

    const category_id = this.$el.find('#thread-category').val();

    let state = '';
    if (level === 'state') {
      state = this.$el.find('#thread-state').val();
    }
    if (title && summary && category_id) {
      $.ajax({
        url: '/api/new_thread/',
        type: 'POST',
        data: {
          title,
          summary,
          category_id,
          level,
          state,
        },
        success(response) {
          if (_this.imageMode === 'upload') {
            const file = $('#id_attachment_image').val();

            if (file) {
              const formData = new FormData(_this.$('#attachment_image_form')[0]);
              formData.set('thread_id', response.thread_id);
              $.ajax({
                url: '/api/upload_image/',
                type: 'POST',
                success() {
                  Materialize.toast('New thread created.', 5000);
                  window.location = `thread/${response.thread_id}`;
                },
                error(e) {
                  Materialize.toast('ERROR: Image could not be uploaded', 5000);
                  Materialize.toast(e.statusText, 5000);
                },
                data: formData,
                cache: false,
                contentType: false,
                processData: false,
              });
            }
          } else if (_this.imageMode === 'link') {
            const img_url = _this
              .$('#link-image-form')
              .val()
              .trim();
            console.log(_this.imageMode, img_url);
            if (img_url) {
              $.ajax({
                url: '/api/upload_image/',
                type: 'POST',
                data: {
                  link: img_url,
                  thread_id: response.thread_id,
                },
                success() {
                  Materialize.toast('New thread created.', 5000);
                  window.location = `thread/${response.thread_id}`;
                },
                error(e) {
                  Materialize.toast('ERROR: Image could not be uploaded', 5000);
                  Materialize.toast(e.statusText, 5000);
                },
              });
            }
          } else {
            Materialize.toast('New thread created.', 5000);
            window.location = `thread/${response.thread_id}`;
          }
        },
      });
    } else {
      Materialize.toast('Please input all fields.', 5000);
    }
  },

  draftThread() {
    const _this = this;

    const title = this.$el.find('#thread-title').val();

    const summary = this.$el.find('#thread-body').val();

    const level = this.$el.find('#thread-location').val();

    const category_id = this.$el.find('#thread-category').val();

    let state = '';
    if (level === 'state') {
      state = this.$el.find('#thread-state').val();
    }
    if (title && summary && category_id) {
      $.ajax({
        url: '/api/new_thread/',
        type: 'POST',
        data: {
          title,
          summary,
          category_id,
          level,
          state,
          is_draft: 'True',
        },
        success(response) {
          if (_this.imageMode === 'upload') {
            const file = $('#id_attachment_image').val();

            if (file) {
              const formData = new FormData(_this.$('#attachment_image_form')[0]);
              formData.set('thread_id', response.thread_id);
              $.ajax({
                url: '/api/upload_image/',
                type: 'POST',
                success() {
                  Materialize.toast('New thread created.', 5000);
                  window.location = `thread/${response.thread_id}`;
                },
                error(e) {
                  Materialize.toast('ERROR: Image could not be uploaded', 5000);
                  Materialize.toast(e.statusText, 5000);
                },
                data: formData,
                cache: false,
                contentType: false,
                processData: false,
              });
            }
          } else if (_this.imageMode === 'link') {
            const img_url = _this
              .$('#link-image-form')
              .val()
              .trim();
            console.log(_this.imageMode, img_url);
            if (img_url) {
              $.ajax({
                url: '/api/upload_image/',
                type: 'POST',
                data: {
                  link: img_url,
                  thread_id: response.thread_id,
                },
                success() {
                  Materialize.toast('New thread created.', 5000);
                  window.location = `thread/${response.thread_id}`;
                },
                error(e) {
                  Materialize.toast('ERROR: Image could not be uploaded', 5000);
                  Materialize.toast(e.statusText, 5000);
                },
              });
            }
          } else {
            Materialize.toast('New thread created.', 5000);
            window.location = `thread/${response.thread_id}`;
          }
        },
      });
    } else {
      Materialize.toast('Please input all fields.', 5000);
    }
  },
});

cw.CategoriesView = BB.View.extend({
  el: '.categories-modal-holder',
  template: _.template($('#categories-template').html()),

  initialize(options) {
    this.categories = options.categories;
    this.user_categories = options.user_categories;
    this.mainView = options.mainView;

    this.render();
  },

  render() {
    this.$el
      .empty()
      .append(
        this.template({ categories: this.categories, user_categories: this.user_categories }),
      );
    cw.materializeShit();
  },

  show() {
    this.$('.categories-modal').openModal();
  },

  hide() {
    this.$('.categories-modal').closeModal();
  },

  events: {
    'click .change-category': 'changeCategory',
    // 'click .create-new-thread': 'createThread'
  },

  changeCategory() {
    const _this = this;

    const selectedCategories = [];
    this.$('input:checked').each(function () {
      selectedCategories.push($(this).val());
    });
    if (selectedCategories.length > 0) {
      $.ajax({
        url: '/api/edit_user_categories/',
        type: 'POST',
        data: {
          'categories[]': selectedCategories,
        },
        success(response) {
          Materialize.toast('Categories Changed', 5000);
          _this.hide();
          _this.user_categories = response.result.user_categories;
          _this.mainView.setUserCategories(_this.user_categories);
          _this.mainView.options.threads.fetch();
          _this.render();
        },
      });
    } else {
      Materialize.toast('Please select at least one category', 5000);
    }
  },
});

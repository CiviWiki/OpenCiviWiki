cw = cw || {};

cw.FeedThreadModel = BB.Model.extend({
    defaults: {
        thread: {
            id: "No Type",
            title: "Civi Title",
            summary: "Thread Summary",
            created: "No Date",
            category_id: 20, // ID for "Other"
            image: "static/img/no_image_md.png"
        },
        author: {
            username: "None",
            full_name: "No Name",
            profile_image: "static/img/no_image_md.png"
        },
        stats: {
            num_views: 0,
            num_civis: 0,
            num_solutions: 0
        }
    }
});

cw.FeedThreadCollection = BB.Collection.extend({
    model: cw.FeedThreadModel,

    url: function () {
        return '/api/feed/';
    },

    filterCategory: function (category_id) {
        var filtered = this.models.filter(function (thread_data) {
            return thread_data.get("thread").category_id === category_id;
        });
        return filtered;
    },
});

cw.FeedView = BB.View.extend({
    el: '#feed',
    template: _.template($('#feed-template').html()),
    feedListTemplate:  _.template($('#feed-list-template').html()),

    initialize: function (options) {
        var _this = this;
        this.options = options || {};
        this.categories = this.options.categories;
        this.threads = this.options.threads.toJSON();
        this.draft_threads = this.options.draft_threads.toJSON();
        this.render();

        this.options.threads.on('sync', function() {
            _this.threads = _this.options.threads.toJSON();
            _this.render();
        });
    },

    render: function () {
        var user_categories = this.options.user_categories;
        var filtered_categories = _.filter(this.options.categories, function(c){ return _.contains(user_categories, c.id); }, user_categories);

        var template_var = {
            'trending': this.options.trending,
            'draft_threads': this.draft_threads,
            'categories': this.options.categories,
            'user_categories': filtered_categories,
        };
        this.$el.empty().append(this.template(template_var));

        this.renderNav();
        this.renderModals();
        this.renderFeedList();
    },

    renderNav: function() {
        this.updatePriorityNav();
        $(window).on("resize", this.updatePriorityNav.bind(this));
    },

    renderModals: function(){
        this.newThreadView = new cw.NewThreadView({
            info: this.options
        });

        this.CategoriesView = new cw.CategoriesView({
            categories: this.options.categories,
            user_categories: this.options.user_categories,
            mainView : this
        });
    },

    renderFeedList: function() {
        var categories = this.options.categories;

        // Annotate each thread with category name
        var annotatedThreads = this.threads.map(function(thread) {
          var thread_category_id = thread.thread.category_id;

          var filtered_categories = categories.filter(function (category) {
              var thread_category_match = category.id === thread_category_id;

              return thread_category_match;
          });
          
          if (filtered_categories.length === 1) {
            thread.thread.category_name = filtered_categories[0].name;
          } else {
            thread.thread.category_name = "ambiguous category";
          }

          return thread;
        });
    
        var template_var = {
          threads: this.threads
        };
    
        this.$("#feed-list")
          .empty()
          .append(this.feedListTemplate(template_var));
        this.$(".scroll-col").height($(window).height() - this.$("nav").height());
      },

    setUserCategories: function (new_list) {
        this.options.user_categories = new_list;
        return this;
    },

    updatePriorityNav: function() {
        var dropdown = this.$('#categories-dropdown');
        var navWidth = this.$('#user-categories-list > li.dropdown-wrapper').width() + this.$('#user-categories-list > li.category-all').width();
		var containerWidth = this.$('.nav-categories').width();

		this.$('#user-categories-list > li.user-categories').each(function() {
			navWidth += $(this).width();
		});

		if (navWidth > containerWidth) {
			var lastItem = this.$('#user-categories-list > li.user-categories').last();
            if (lastItem.text()){
                lastItem.attr('data-width', lastItem.width());
                dropdown.prepend(lastItem);
    			this.updatePriorityNav();
            }

		} else {
    		var firstDropdownElement = dropdown.children().first();
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

    filterFeed: function(e) {
        var target = $(e.target);
        var selectedCategory = target.data('id');
        if (selectedCategory === "arrow") {
            return;
        } else {
            if (selectedCategory === "all"){
                this.threads = this.options.threads.toJSON();
            } else if (_.contains(this.options.user_categories, selectedCategory)) {
                this.threads = JSON.parse(JSON.stringify(this.options.threads.filterCategory(selectedCategory)));
            }
            this.renderFeedList();
            this.$('.category-item').removeClass('active');
            target.addClass('active');
        }
    },

    allFeed: function() {
        this.$('.category-item').removeClass('active');
        this.$('.category-all > .category-item').addClass('active');
    },

    openNewThreadModal: function () {
        this.newThreadView.show();
    },
    openCategoryModal: function() {
        this.CategoriesView.show();
    }
});

cw.NewThreadView = BB.View.extend({
    el: '.new-thread-modal-holder',
    template: _.template($('#new-thread-template').html()),

    initialize: function (options) {
        this.options = options.info;
        this.imageMode = "";
        this.render();
    },

    render: function () {
        this.$el.empty().append(this.template());
        cw.materializeShit();
    },

    show: function () {
        this.$('.new-thread-modal').openModal();
    },

    hide: function () {
        this.$('.new-thread-modal').closeModal();
    },

    events: {
        'click .cancel-new-thread': 'cancelThread',
        'click .create-new-thread': 'createThread',
        'click #image-from-computer': 'showImageUploadForm',
        'click #image-from-link': 'showImageLinkForm',
        'change #thread-location': 'showStates',
    },

    cancelThread: function () {
        this.hide();
    },
    showImageUploadForm: function () {
        this.imageMode="upload";
        this.$('#attachment_image_form').removeClass('hide');
        this.$('#link-image-form').addClass('hide');
    },
    showImageLinkForm: function () {
        this.imageMode="link";
        this.$('#attachment_image_form').addClass('hide');
        this.$('#link-image-form').removeClass('hide');
    },

    createThread: function () {
        var _this = this;

        var title = this.$el.find('#thread-title').val(),
            summary = this.$el.find('#thread-body').val(),
            category_id = this.$el.find('#thread-category').val();

        if (title && summary && category_id) {
            $.ajax({
                url: '/api/new_thread/',
                type: 'POST',
                data: {
                    csrfmiddlewaretoken: csrftoken,
                    title: title,
                    summary: summary,
                    category_id: category_id
                },
                success: function (response) {
                    if (_this.imageMode==="upload") {
                        var file = $('#id_attachment_image').val();

                        $.ajaxSetup({
                            beforeSend: function(xhr, settings) {
                                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                                }
                            }
                        });

                        if (file) {
                            var formData = new FormData(_this.$('#attachment_image_form')[0]);
                            formData.set('thread_id', response.thread_id);
                            $.ajax({
                                url: '/api/upload_image/',
                                type: 'POST',
                                success: function () {
                                    Materialize.toast('New thread created.', 5000);
                                    window.location = "thread/" + response.thread_id;
                                },
                                error: function(e){
                                    Materialize.toast('ERROR: Image could not be uploaded', 5000);
                                    Materialize.toast(e.statusText, 5000);
                                },
                                data: formData,
                                cache: false,
                                contentType: false,
                                processData: false
                            });
                        }
                    } else if (_this.imageMode==="link") {
                        var img_url = _this.$('#link-image-form').val().trim();
                        console.log(_this.imageMode, img_url);
                        if (img_url) {
                            $.ajax({
                                url: '/api/upload_image/',
                                type: 'POST',
                                data: {
                                    csrfmiddlewaretoken: csrftoken,
                                    link: img_url,
                                    thread_id: response.thread_id
                                },
                                success: function () {
                                    Materialize.toast('New thread created.', 5000);
                                    window.location = "thread/" + response.thread_id;
                                },
                                error: function(e){
                                    Materialize.toast('ERROR: Image could not be uploaded', 5000);
                                    Materialize.toast(e.statusText, 5000);
                                }
                            });
                        }
                    } else {
                        Materialize.toast('New thread created.', 5000);
                        window.location = "thread/" + response.thread_id;
                    }

                }
            });
        } else {
            Materialize.toast('Please input all fields.', 5000);
        }
    },
});


cw.CategoriesView = BB.View.extend({
    el: '.categories-modal-holder',
    template: _.template($('#categories-template').html()),

    initialize: function (options) {
        this.categories = options.categories;
        this.user_categories = options.user_categories;
        this.mainView = options.mainView;

        this.render();
    },

    render: function () {
        this.$el.empty().append(this.template({categories: this.categories, user_categories: this.user_categories}));
        cw.materializeShit();
    },

    show: function () {
        this.$('.categories-modal').openModal();
    },

    hide: function () {
        this.$('.categories-modal').closeModal();
    },

    events: {
        'click .change-category': 'changeCategory',
        // 'click .create-new-thread': 'createThread'
    },

    changeCategory: function () {
        var _this = this;

        var selectedCategories = [];
        this.$("input:checked").each(function() {
           selectedCategories.push($(this).val());
        });
        if (selectedCategories.length > 0) {
            $.ajax({
                url: '/api/edit_user_categories/',
                type: 'POST',
                data: {
                    'categories[]': selectedCategories,
                },
                success: function (response) {
                    Materialize.toast('Categories Changed', 5000);
                    _this.hide();
                    _this.user_categories = response.result.user_categories;
                    _this.mainView.setUserCategories(_this.user_categories);
                    _this.mainView.options.threads.fetch();
                    _this.render();
                }
            });
        } else {
            Materialize.toast('Please select at least one category', 5000);
        }
    },
});

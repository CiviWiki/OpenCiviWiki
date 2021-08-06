cw = cw || {};

cw.AccountModel = BB.Model.extend({
    defaults: function() {
        return {
            profile_image: "",
            username: "",
            first_name: "",
            last_name: "",
            about_me: "",
            location: "",
            history: [],
            followers: [],
            following: [],
            issues: [],
        };
    },
    url: function () {
        if (! this.user ) {
            throw new Error("This is a race condition! and why we can't have nice things :(");
        }
        return '/api/account_profile/' + this.user + '/';
    },

    initialize: function (model, options) {
        options = options || {};
        this.user = options.user;
    }
});


// And hereon commences a pile of horrendous code. Beware!
// TODO: review rewrite refactor. (please)
cw.AccountView = BB.View.extend({
    el: '#account',
    template: _.template($('#account-template').html()),
    settingsTemplate: _.template($('#settings-template').html()),
    sidebarTemplate: _.template($('#sidebar-template').html()),

    // Account Tabs Templates
    mycivisTemplate: _.template($('#my-civis-template').html()),
    followersTemplate: _.template($('#followers-template').html()),
    followingTemplate: _.template($('#following-template').html()),
    myissuesTemplate: _.template($('#my-issues-template').html()),

    // Partials
    userCardTemplate: _.template($('#user-card-template').html()),


    initialize: function (options) {
        options = options || {};
        this.current_user = options.current_user;
        this.isSave = false;

        this.listenTo(this.model, 'sync', function(){
            document.title = this.model.get("first_name") +" "+ this.model.get("last_name") +" (@"+this.model.get("username")+")";

            this.postRender();

            if (_.find(this.model.get("followers"), function(follower){
                return (follower.username== current_user);
            })) {
                var follow_btn = this.$('#sidebar-follow-btn');
                follow_btn.addClass("btn-secondary");
                follow_btn.data("follow-state", true);
                follow_btn.html("");
            }
        });

        return this;
    },

    render: function () {
        if (this.isSave) {
            this.postRender();
        } else {
            this.$el.empty().append(this.template());

            $('.account-tabs .tab').on('dragstart', function() {return false;});
            this.$el.find('.account-settings').pushpin({ top: $('.account-settings').offset().top });
            this.$el.find('.scroll-col').height($(window).height());
        }
    },

    tabsRender: function () {
        this.$('#civis').empty().append(this.mycivisTemplate());
        this.$('#followers').empty().append(this.followersTemplate());
        this.$('#following').empty().append(this.followingTemplate());
        this.$('#issues').empty().append(this.myissuesTemplate());
        var settingsEl = this.$('#settings');
        if (settingsEl.length) {
            settingsEl.empty().append(this.settingsTemplate());
            Materialize.updateTextFields();
        }
    },

    postRender: function () {
        // Timestamp the image with a cachebreaker so that proper refersh occurs
        this.model.set({"profile_image": this.model.get("profile_image") + "?" + new Date().getTime() });
        this.$el.find('.account-settings').empty().append(this.sidebarTemplate());
        this.tabsRender();
        cw.materializeShit();
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
        'keypress .save-account': cw.checkForEnter,
    },

    toggleSolutions: function(e) {
        var id = $(e.currentTarget).data('id');
        var textElement = $(e.currentTarget).find('.button-text');
        var new_text = textElement.text() === "Show Solutions" ? "Hide Solutions" : "Show Solutions";
        textElement.text(new_text);
        this.$('#solutions-'+id).toggleClass('hide');
    },

    previewImage: function(e){
        var _this = this;
        var img = this.$el.find('#id_profile_image');
        if (img.val()) {
            var uploaded_image = img[0].files[0];
            if (uploaded_image) {
                var formData = new FormData(this.$el.find('#profile_image_form')[0]);

                var reader = new FileReader();

                reader.onload = function(e) {
                    var preview_image = _this.$el.find('.preview-image');
                    preview_image.attr('src', e.target.result);

                    _this.toggleImgButtons();
                };
                reader.readAsDataURL(uploaded_image);
            }
        }
    },

    showUserCard: function(e) {
        var _this = this;
        var username = e.currentTarget.dataset.username;
        if (!$('#usercard-'+ username).hasClass('open')) {
            clearTimeout(this.showTimeout);
            this.showTimeout = setTimeout(function() {
                $.ajax({
                    type: 'POST',
                    url: '/api/account_card/'+username,
                    success: function (data) {
                        data.isCurrentUser = false;
                        if (current_user == data.username){
                            data.isCurrentUser = true;
                        }
                        _this.$(e.currentTarget).parent().after(_this.userCardTemplate(data));
                        // Hover Elements
                        var target = _this.$(e.currentTarget),
                            targetCard = _this.$('#usercard-'+ username);

                        targetCard.stop().fadeIn("fast", function(){
                            // Positions
                            var pos = target.offset(),
                            // Dimenions
                                cardWidth = targetCard.width(),
                                cardHeight = targetCard.height(),
                                chipHeight = target.height(),
                                documentHeight = $(window).height(),
                                scroll = _this.$(".scroll-col").scrollTop(),
                                top,left;

                            if (target[0].getBoundingClientRect().top + cardHeight + chipHeight >= documentHeight) {
                                top = pos.top + scroll - cardHeight - chipHeight -2;
                            } else {
                                top = pos.top + scroll + 25;
                            }
                            left = target.position().left + 20;

                            // Determine placement of the hovercard
                            targetCard.css({
                                'top': top ,
                                'left': left
                            });
                        }).addClass('open');
                    },
                    error: function () {
                        // No card for you!
                        return;
                    }
                });
            }, 200);
        }
    },

    hideUserCard: function(e) {
        var _this = this,
            username = e.currentTarget.dataset.username,
            card = this.$('.user-card');
        if (('timeout-'+username) in this){
            clearTimeout(this['timeout-'+username]);
        }
        clearTimeout(this.showTimeout);
        this['timeout-'+username] = setTimeout(function() {
            card.fadeOut("fast",function(){$(this).remove();});
        }, 200);
        $('#usercard-'+ username).hover(function() {
            if (('timeout-'+username) in _this){
                clearTimeout(_this['timeout-'+username]);
            }
        }, function() {
            if (('timeout-'+username) in _this){
                clearTimeout(_this['timeout-'+username]);
            }
            _this['timeout-'+username] = setTimeout(function() {
                card.fadeOut("fast",function(){$(this).remove();});
            }, 100);
        });
    },

    showRawRatings: function(e) {
        $(e.target).closest('.rating').find('.rating-score').toggleClass('hide');
        $(e.target).closest('.rating').find('.rating-percent').toggleClass('hide');
    },

    toggleImgButtons: function(event) {
        this.$('.profile-image-pick').toggleClass('hide');
        this.$('.upload-image').toggleClass('hide');
        this.$('#confirmation-prompt').toggleClass('hide');
    },

    followRequest: function(e){
        var apiData = {},
            _this = this,
            follow_state = this.$(e.currentTarget).data("follow-state");
            target = this.$(e.target);

        apiData.target = this.$(e.currentTarget).data("username");

        if (!follow_state) {
            $.ajax({
                url: '/api/follow/',
                type: 'POST',
                data: apiData,
                success: function () {
                    Materialize.toast('You are now following user '+ apiData.target, 5000);
                    target.addClass("btn-secondary");
                    target.data("follow-state", true);
                    target.html("");

                },
                error: function () {
                    Materialize.toast('Could not follow user '+ apiData.target, 5000);
                }
            });
        } else {
            $.ajax({
                url: '/api/unfollow/',
                type: 'POST',
                data: apiData,
                success: function () {
                    Materialize.toast('You have unfollowed user '+ apiData.target, 5000);
                    target.removeClass("btn-secondary");
                    target.html("FOLLOW");
                    target.data("follow-state", false);
                },
                error: function () {
                    Materialize.toast('Could not unfollow user '+ apiData.target, 5000);
                }
            });
        }

    },

    saveAccount: function (e) {
        var $this = $(e.target),
            changeKey = $this.attr('id'),
            changeVal = $this.val().trim(),
            apiData = {},
            _this = this;

        if (this.model.get([changeKey]) === changeVal) {
            return;
        }

        apiData[changeKey] = changeVal;

        $.ajax({
            url: '/api/edituser/',
            type: 'POST',
            data: apiData,
            success: function () {
                Materialize.toast('Saved!', 5000);

                _this.isSave = true;
                _this.model.fetch();

            }
        });
    },
    
    handleFiles: function(e) {
        e.preventDefault();

        var _this = this,
            formData = new FormData($('#profile_image_form')[0]);

        $.ajax({
            url: '/api/upload_profile/',
            type: 'POST',
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
            success: function () {
                Materialize.toast('Saved!', 5000);

                _this.isSave = true;
                _this.model.fetch();
            },
            error: function(data){
                if (data.status === 400) {
                    Materialize.toast(data.responseJSON.message, 5000, 'red');
                } else if (data.status === 500) {
                    Materialize.toast('Internal Server Error', 5000, 'red');
                } else {
                    Materialize.toast(data.statusText, 5000, 'red');
                }
            },

        });
        this.toggleImgButtons();

        return false;
    },
});

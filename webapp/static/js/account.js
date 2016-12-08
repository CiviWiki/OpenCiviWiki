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
            representatives: []
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


// And hereon commences a pile of horrendous code. Be Ware!
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
    myrepsTemplate: _.template($('#my-reps-template').html()),
    mybillsTemplate: _.template($('#my-bills-template').html()),


    initialize: function (options) {
        options = options || {};
        this.mapView = options.mapView;
        this.isSave = false;

        this.listenTo(this.model, 'sync', function(){
            document.title = this.model.get("first_name") +" "+ this.model.get("last_name") +" (@"+this.model.get("username")+")";

            this.postRender();

            if (_.find(this.model.get("followers"), function(follower){
                return (JSON.parse(follower).username== current_user);
            })) {
                var follow_btn = this.$el.find('.follow-btn');
                follow_btn.addClass("disabled");
                follow_btn.removeClass("follow-btn waves-effect waves-light");
                follow_btn.html("FOLLOWING");
            }
        });

        return this;
    },

    render: function () {
        if (this.isSave) {
            this.postRender();
        } else {
            this.$el.empty().append(this.template());
            this.$el.find('.account-settings').pushpin({ top: $('.account-settings').offset().top });
            this.$el.find('.scroll-col').height($(window).height());
        }

        // Only render the settings form if logged in user
        var settingsEl = this.$('#settings');
        if (settingsEl.length) {
            settingsEl.empty().append(this.settingsTemplate());
            this.mapView.renderAndInitMap();
            this.listenTo(this.mapView.model, 'change', _.bind(this.saveLocation, this)); //TODO: validateLocation and then save
        }
    },

    tabsRender: function () {
        this.$('#civis').empty().append(this.mycivisTemplate());
        this.$('#followers').empty().append(this.followersTemplate());
        this.$('#following').empty().append(this.followingTemplate());
        this.$('#issues').empty().append(this.myissuesTemplate());
        this.$('#myreps').empty().append(this.myrepsTemplate());
        this.$('#mybills').empty().append(this.mybillsTemplate());

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
        'change .profile-image-pick': 'toggleImgButtons',
        'blur .save-account': 'saveAccount',
        'keypress .save-account': cw.checkForEnter,
    },
    showRawRatings: function(e) {
        $(e.target).closest('.rating').find('.rating-score').toggleClass('hide');
        $(e.target).closest('.rating').find('.rating-percent').toggleClass('hide');
    },

    toggleImgButtons: function(event) {
        this.$('.profile-image-pick').toggleClass('hide');
        this.$('.upload-image').toggleClass('hide');
    },

    followRequest: function(e){
        var apiData = {},
            _this = this;
        apiData.from_user = this.user;
        apiData.to_user = this.user;

        $.ajax({
            url: '/api/followUser/',
            type: 'POST',
            data: apiData,
            success: function () {
                Materialize.toast('You are now following '+_this.model.get("first_name")+" "+_this.model.get("last_name"), 3000);


                $(e.target).removeClass("follow-btn waves-effect waves-light");
                $(e.target).html("FOLLOWING");
            }
        });
        $(e.target).addClass("disabled");
    },

    saveAccount: function (e) {
        var $this = $(e.target),
            changeKey = $this.attr('id'),
            changeVal = $this.val(),
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
                Materialize.toast('Saved!', 3000);

                _this.isSave = true;
                _this.model.fetch();

            }
        });
    },
    saveLocation: function () {
        var _this = this;

        var coordinates = this.mapView.model.get('coordinates'),
            address = this.mapView.model.get('address');

        if (!_.isEmpty(coordinates) && !_.isEmpty(address)) {
            $.ajax({
                type: 'POST',
                url: '/api/edituser/',
                data: {
                    coordinates: coordinates,
                    address: address.address,
                    city: address.city,
                    state: address.state,
                    zip_code: address.zipcode,
                    longitude: coordinates.lng,
                    latitude: coordinates.lat,
                },
                success: function (data) {
                    Materialize.toast('<span class="subtitle-lato white-text">Location Changed</span>', 3000);
                    _this.isSave = true;
                    _this.model.fetch();
                },
                error: function (data) {
                    if (data.status_code === 400) {
                        Materialize.toast(data.message, 3000);
                    } else if (data.status_code === 500) {
                        Materialize.toast('Internal Server Error', 3000);
                    } else {
                        Materialize.toast(data.statusText, 2000);
                    }
                }
            });
        }
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
                console.log("succ"+JSON.stringify(formData));
                Materialize.toast('Saved!', 3000);

                _this.isSave = true;
                _this.model.fetch();
            },
            error: function(e){
                Materialize.toast('ERROR: Image could not be uploaded', 3000);
                Materialize.toast(JSON.stringify(e), 3000);
            },

        });
        this.toggleImgButtons();

        return false;
    },
    // // SunlightAPI related functions
    // getLegislators: function(coordinates){
    //     var _this = this;
    //     $.ajax({
    //         url: "https://congress.api.sunlightfoundation.com/legislators/locate?latitude=" + coordinates.lat + "&longitude="+ coordinates.lng + "&callback=?",
    //         headers:{"X-APIKEY": this.sunlightApiKey},
    //         dataType: "jsonp",
    //         success: function(data, status){
    //             _this.$('#rep-list').empty();
    //             _.each(data.results, function(rep){
    //                 _this.$('#rep-text').addClass('hide');
    //                 _this.$('#rep-list').append(_this.repChipTemplate({ rep : rep }));
    //             });
    //         },
    //         error: function(){
    //             Materialize.toast("Sunlight Error: Could not get representatives", 2000);
    //         }
    //     });
    // }
});

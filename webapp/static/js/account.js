cw = cw || {};

cw.AccountModel = BB.Model.extend({
    defaults: function() {
        return {
            profile_image: "",
            username: "",
            first_name: "",
            last_name: "",
            about_me: "",
            zip_code: "",
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
        this.isSave = false;

        this.listenTo(this.model, 'sync', function(){
            console.log(this.model);
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

        this.render();
    },

    render: function () {
        if (this.isSave) {
            this.postRender();
        } else {
            this.$el.empty().append(this.template());
            this.$el.find('.account-settings').pushpin({ top: $('.account-settings').offset().top });
            this.$el.find('.scroll-col').height($(window).height());
        }
    },

    tabsRender: function () {
        this.$('#civis').empty().append(this.mycivisTemplate());
        this.$('#followers').empty().append(this.followersTemplate());
        this.$('#following').empty().append(this.followingTemplate());
        this.$('#issues').empty().append(this.myissuesTemplate());
        this.$('#myreps').empty().append(this.myrepsTemplate());
        this.$('#mybills').empty().append(this.mybillsTemplate());
        this.$('#settings').empty().append(this.settingsTemplate());
    },

    postRender: function () {
        this.$el.find('.account-settings').empty().append(this.sidebarTemplate());
        this.tabsRender();
        cw.materializeShit();




        this.isSave = false;
    },

    events: {
        // 'mouseenter .rating-box ': 'showRawRatings',
        // 'mouseleave .rating-box ': 'showRawRatings',
        'click .settings': 'showSettings',
        'click .follow-btn': 'followRequest',
        'blur .save-account': 'saveAccount',
        'keypress .save-account': cw.checkForEnter
    },
    showRawRatings: function(e) {
        $(e.target).closest('.rating').find('.rating-score').toggleClass('hide');
        $(e.target).closest('.rating').find('.rating-percent').toggleClass('hide');
    },

    showSettings: function(event) {
        console.log("settings");
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

                $(e.target).addClass("disabled");
                $(e.target).removeClass("follow-btn waves-effect waves-light");
                $(e.target).html("FOLLOWING");
            }
        });
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

                // _this.isSave = true;
                // _this.model.fetch();
            }
        });
    },

});

cw = cw || {};

cw.AccountModel = BB.Model.extend({
    url: function () {
            if (! this.user ) {
                throw new Error("This is a race condition! and why we can't have nice things :(");
            }
            return '/api/account_data/' + this.user + '/';
    },

    initialize: function (model, options) {
        this.user = options.user;
    }
});

cw.AccountView = BB.View.extend({
    el: '#account',
    template: _.template($('#account-template').html()),
    settingsTemplate: _.template($('#settings-template').html()),

    // Account Tabs Templates
    mycivisTemplate: _.template($('#my-civis-template').html()),
    followersTemplate: _.template($('#followers-template').html()),
    followingTemplate: _.template($('#following-template').html()),
    myissuesTemplate: _.template($('#my-issues-template').html()),
    myrepsTemplate: _.template($('#my-reps-template').html()),

    initialize: function (options) {
        this.isSave = false;

        this.listenTo(this.model, 'sync', function(){
            console.log(this.model);
            this.postRender();
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
    },

    postRender: function () {
        this.$el.find('.account-settings').empty().append(this.settingsTemplate());
        this.tabsRender();
        cw.materializeShit();
        this.isSave = false;
    },

    events: {
        'blur .save-account': 'saveAccount',
        'keypress .save-account': cw.checkForEnter
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

});

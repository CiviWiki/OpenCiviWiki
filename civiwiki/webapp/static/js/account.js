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

    initialize: function () {
        this.listenTo(this.model, 'sync', this.render);
    },

    render: function () {
        this.$el.empty().append(this.template());
        this.$el.find('.scroll-col').height($(window).height());
        cw.materializeShit();
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
                _this.model.fetch();
            }
        });
    },

});

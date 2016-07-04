cw = cw || {};

cw.AccountView = BB.View.extend({
    el: '#account',
    template: _.template($('#account-template').html()),

    initialize: function () {
        this.render();
    },

    render: function () {
        this.$el.empty().append(this.template());
        this.$el.find('.scroll-col').height($(window).height());
    },

    events: {
        'blur .save-account': 'saveAccount',
        'keypress .save-account': cw.checkForEnter
    },

    saveAccount: function (e) {
        var $this = $(e.target),
            changeKey = $this.attr('id'),
            changeVal = $this.val(),
            apiData = {};

        if (this.model.get('profile')[changeKey] === changeVal) {
            return;
        }

        apiData[changeKey] = changeVal;

        this.model.fetch({
            url: 'api/edituser',
            type: 'POST',
            data: apiData
        });
    },

});

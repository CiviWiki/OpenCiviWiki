cw = cw || {};

cw.FeedView = BB.View.extend({
    el: '#feed',
    template: _.template($('#feed-template').html()),

    initialize: function () {
        this.render();
    },

    render: function () {
        this.$el.empty().append(this.template());
    },

    events: {
        'click .account-button': 'goToAccount'
    },

    goToAccount: function () {
        window.location.href = '/account';
    }
});

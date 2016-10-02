cw = cw || {};

cw.FeedView = BB.View.extend({
    el: '#feed',
    template: _.template($('#feed-template').html()),

    initialize: function (options) {
        this.username = options.username;

        this.render();
    },

    render: function () {
        this.$el.empty().append(this.template());
    },

    events: {
    },
});

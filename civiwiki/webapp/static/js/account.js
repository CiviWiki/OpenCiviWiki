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
    },

});

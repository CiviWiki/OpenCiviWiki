cw = cw || {};

cw.LandingView = BB.View.extend({
    el: '#landing',
    landingTemplate: _.template($('#landing-template').html()),

    initialize: function () {
        this.render();
    },

    render: function () {
        this.$el.empty().append(this.landingTemplate());
    },
});

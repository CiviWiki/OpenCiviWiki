cw = cw || {};

cw.SupportusView = BB.View.extend({
    el: '#supportus',
    supportusTemplate: _.template($('#supportus-template').html()),

    initialize: function () {
        this.render();
    },

    render: function () {
        this.$el.empty().append(this.supportusTemplate());
        this.setupStaticNav();
        $('.parallax').parallax();
    },

    // Setup sidebar functionality
    setupStaticNav: function () {
        $('.button-collapse').sideNav();
        $('.collapsible').collapsible();
    }
});

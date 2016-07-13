cw = cw || {};

cw.HowItWorksView = BB.View.extend({
    el: '#howitworks',
    howitworksTemplate: _.template($('#howitworks-template').html()),

    initialize: function () {
        this.render();
    },

    render: function () {
        this.$el.empty().append(this.howitworksTemplate());
        this.setupStaticNav();
    },

    setupStaticNav: function () {
        $('.button-collapse').sideNav();
        $('.collapsible').collapsible();
        $('.sideNav').css('display', 'inherit');
    }
});

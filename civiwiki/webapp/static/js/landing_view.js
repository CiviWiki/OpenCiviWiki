cw = cw || {};

cw.LandingView = BB.View.extend({
    el: '#landing',
    landingTemplate: _.template($('#landing-template').html()),

    initialize: function () {
        this.render();
    },

    render: function () {
        this.$el.empty().append(this.landingTemplate());

        // Adjusts the height of a div to the window size if larger than default
        this.$el.find('.full-height').height(
            function(){
                return (_.max([$(this).height(), $(window).height()]) + "px");
            }
        );

        this.setupStaticNav();
    },

    setupStaticNav: function () {
        $('.button-collapse').sideNav();
        $('.collapsible').collapsible();
        $('.sideNav').css('display', 'inherit');
    }
});

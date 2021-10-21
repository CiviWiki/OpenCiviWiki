cw = cw || {};
Materialize = M
Materialize.AutoInit()
cw.LandingView = BB.View.extend({
    el: '#landing',
    landingTemplate: _.template($('#landing-template').html()),

    initialize: function () {
        this.render();
    },

    render: function () {
        this.$el.empty().append(this.landingTemplate());

        this.setupStaticNav();
    },

    
    setupStaticNav: function () {
        
        // $('.sidenav').sidenav();
        // $('.collapsible').collapsible();
        $('.sidenav').css('display', 'inherit');
        
    }
});

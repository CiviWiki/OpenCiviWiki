cw = cw || {};
Materialize = M
Materialize.AutoInit()
cw.AboutView = BB.View.extend({
    el: '#about',
    aboutTemplate: _.template($('#about-template').html()),

    initialize: function () {
        this.render();
    },

    render: function () {
        this.$el.empty().append(this.aboutTemplate());
        this.setupStaticNav();
    },

    setupStaticNav: function () {
        // $('.sidenav').sidenav();
        // $('.collapsible').collapsible();
        $('.sidenav').css('display', 'inherit');
    }
});

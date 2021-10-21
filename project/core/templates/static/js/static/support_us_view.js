cw = cw || {};
Materialize = M
Materialize.AutoInit()
cw.SupportusView = BB.View.extend({
    el: '#supportus',
    supportusTemplate: _.template($('#supportus-template').html()),

    initialize: function () {
        this.render();
    },

    render: function () {
        this.$el.empty().append(this.supportusTemplate());
        this.setupStaticNav();
        // $('.parallax').parallax();
    },

    // Setup sidebar functionality
    setupStaticNav: function () {
        // $('.button-collapse').sidenav();
        // $('.collapsible').collapsible();
        $('.sidenav').css('display', 'inherit');

    }
});

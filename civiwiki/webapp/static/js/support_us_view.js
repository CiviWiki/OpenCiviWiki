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
        // Following initializes parallax, an effect where the background moves slower than the foreground
        $('.parallax').parallax();

        // Code to configure twitter sharing from the twitter website
        !function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+'://platform.twitter.com/widgets.js';fjs.parentNode.insertBefore(js,fjs);}}(document, 'script', 'twitter-wjs');
    },

    setupStaticNav: function () {
        $('.button-collapse').sideNav();
        $('.collapsible').collapsible();
        $('.sideNav').css('display', 'inherit');
    }
});

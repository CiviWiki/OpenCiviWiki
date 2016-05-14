var AboutView = Backbone.View.extend({

    el: '#about',

    initialize: function() {
        this.template = _.template($('#about-template').text());
        this.render();
    },

    render: function() {
        this.$el.html(this.template());
    },

});

var about_view = new AboutView();

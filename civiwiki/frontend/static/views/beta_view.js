//This page isn't being used at the moment. Trying to figure out a way to possibly put this into login_view 
// or to make this an entirely separate page

var BetaView = Backbone.View.extend({

    el: '#beta',

    initialize: function() {
        this.template = _.template($('#beta-template').text());
        this.render();
    },

    render: function() {
        this.$el.html(this.template());
    },

});

var beta_view = new BetaView();
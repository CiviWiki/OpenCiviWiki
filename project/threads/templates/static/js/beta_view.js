cw = cw || {};

cw.BetaView = BB.View.extend({

    el: '#beta',

    initialize: function() {
        this.template = _.template($('#beta-template').text());
        this.render();
    },

    render: function() {
        this.$el.html(this.template());
    },

});

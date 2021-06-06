cw = cw || {};

cw.GeneralView = BB.View.extend({

    el: '#general',

    initialize: function() {
        this.template = _.template($('#general-template').text());
        this.render();
    },

    render: function() {
        this.$el.html(this.template());
    },

});

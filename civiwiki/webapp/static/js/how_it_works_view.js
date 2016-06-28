cw = cw || {};

cw.HowItWorksView = BB.View.extend({
    el: '#howitworks',
    howitworksTemplate: _.template($('#howitworks-template').html()),

    initialize: function () {
        this.render();
    },

    render: function () {
        this.$el.empty().append(this.howitworksTemplate());
    },
});

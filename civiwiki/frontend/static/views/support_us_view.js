var SupportUsView = Backbone.View.extend({

    el: '#supportus',

    initialize: function() {
        this.template = _.template($('#supportus-template').text());
        this.render();
    },

    render: function() {
        this.$el.html(this.template());
    },

});

var support_us_view = new SupportUsView();
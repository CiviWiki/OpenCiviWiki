cw = cw || {};

cw.AccountView = BB.View.extend({
    el: '#account',
    template: _.template($('#account-template').html()),

    initialize: function () {
        this.render();
    },

    render: function () {
        this.$el.empty().append(this.template());
        this.$el.find('.scroll-col').height($(window).height());
    },

    events: {
        'blur .save-account': 'saveAccount',
        'keypress .save-account': 'calcKey'
    },

    calcKey: function (e) {
        if (e.which == 13 && !e.shiftKey) {
            e.preventDefault();
            $(e.target).blur();
        }
    },

    saveAccount: function (e) {
        var $this = $(e.target),
            changeKey = $this.attr('id'),
            changeVal = $this.val(),
            apiData = {};

        apiData[changeKey] = changeVal;

        $.ajax({
            url: 'api/edituser',
            type: 'POST',
            data: apiData
        });
    },

});

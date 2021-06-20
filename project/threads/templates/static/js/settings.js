cw = cw || {};

cw.UserModel = BB.Model.extend({
    defaults: function() {
        return {
            username: "",
            email: "",
        };
    },
    url: function () {
        if (! this.get('username') ) {
            throw new Error("This is a race condition! and why we can't have nice things :(");
        }
        return '/api/account_profile/' + this.get('username') + '/';
    },

    initialize: function (model, options) {
        options = options || {};
    }
});


cw.SettingsView = BB.View.extend({

    el: '#settings',

    initialize: function(options) {
        this.options = options || {};

        this.template = _.template($('#settings-template').text());
        this.settingsTemplate = _.template($('#settings-base').text());
        this.personalTemplate = _.template($('#settings-personal').text());

        this.listenTo(this.model, 'change', this.renderAllLabels);
    },

    render: function() {
        this.$el.html(this.template());

        this.$('#settings-el').html(this.settingsTemplate());

        this.renderPersonal();
    },

    renderAllLabels:function() {
        this.renderPersonal();
        Materialize.updateTextFields();
    },

    renderPersonal: function() {
        this.$('#settings-1').html(this.personalTemplate());
    },

    events: {
        'blur .save-account': 'saveAccount',
    },

    saveAccount: function (e) {
        var $this = $(e.target),
            changeKey = $this.attr('id'),
            changeVal = $this.val().trim(),
            apiData = {},
            _this = this;

        if (this.model.get([changeKey]) === changeVal) {
            return;
        }

        apiData[changeKey] = changeVal;

        $.ajax({
            url: '/api/edituser/',
            type: 'POST',
            data: apiData,
            success: function () {
                Materialize.toast('Saved!', 5000);

                _this.isSave = true;
                _this.model.fetch();

            }
        });
    },
});

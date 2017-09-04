cw = cw || {};

cw.BetaRegisterView = BB.View.extend({
    el: '#beta_register',
    entryTemplate: _.template($('#entry-template').html()),
    registerTemplate: _.template($('#register-template').html()),

    initialize: function () {
        this.render();
    },

    render: function () {
        this.$el.empty().append(this.entryTemplate());
        this.$('#entry-content').empty().append(this.registerTemplate());
    },

    events: {
        'click .register-button': 'register'
    },

    register: function () {
        var email = this.$el.find('#email').val().trim().trim(),
            username = this.$el.find('#username').val().trim(),
            password = this.$el.find('#password').val();

        var beta_token = this.$('#beta_token').val();

        if (!beta_token) {
            Materialize.toast('Missing Beta Token', 5000, 'red');
        }

        if (password && username) {
            $.ajax({
                type: 'POST',
                url: '/auth/beta_register',
                data: {
                    email: email,
                    username: username,
                    password: password,
                    beta_token: beta_token
                },
                success: function () {
                    window.location.replace('/');
                },
                error: function (data) {
                    if (data.status === 400 && data.responseJSON) {
                        _.each(data.responseJSON.errors, function(error){
                            Materialize.toast(error, 5000, 'red');
                        });
                        Materialize.toast(data.responseJSON.message, 5000, 'red');
                    } else {
                        Materialize.toast(data.statusText, 5000, 'red');
                    }
                }
            });

        } else {
            Materialize.toast('Please fill all the fields', 5000, 'red');
        }
    }
});

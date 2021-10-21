cw = cw || {};
Materialize = M
Materialize.AutoInit()
cw.LoginView = BB.View.extend({
    el: '#login',
    entryTemplate: _.template($('#entry-template').html()),
    loginTemplate: _.template($('#login-template').html()),
    registerTemplate: _.template($('#register-template').html()),

    initialize: function () {
        this.register = false;
        this.render();
    },

    render: function () {
        this.$el.empty().append(this.entryTemplate());
        this.renderForms();
    },

    renderForms: function()  {
        if (this.register) {
            this.$('#entry-content').empty().append(this.registerTemplate());
        } else {
            this.$('#entry-content').empty().append(this.loginTemplate());
        }
    },

    events: {
        'click .login-button': 'login',
        'click .register-link': 'swapToRegister',
        'click .login-link': 'swapToLogin',
        'click .register-button': 'register',
        'keypress .login-input ': 'checkForEnter',
        'blur .login-input': 'usernameToLowerCase'
    },

    checkForEnter: function(e) {
        if (e.which == 13 && !e.shiftKey) {
            e.preventDefault();
            this.login();
        }
    },

    usernameToLowerCase: function(e){
        var usernameInput = this.$('#username');
        var lower = usernameInput.val().toLowerCase();
        if (lower != usernameInput.val()) {
            usernameInput.val(lower);
        }
    },

    login: function () {
        var username = this.$el.find('#username').val(),
            password = this.$el.find('#password').val();
        
        if (username && password) {
            $.ajax({
                type: 'POST',
                url: 'auth/login',
                data: {
                    username: username,
                    password: password
                },
                success: function () {
                    window.location.replace('/');
                },
                error: function (data) {
                    if (data.status === 400 && data.responseJSON) {
                        Materialize.toast({html:data.responseJSON.message,displayLength: 5000});
                    } else {
                        Materialize.toast({html:data.statusText,displayLength: 5000});
                    }
                }
            });
        } else {
            Materialize.toast({html:'<span class="subtitle-lato white-text">Please input your username and password</span>',displayLength: 5000});
        }
    },

    swapToRegister: function () {
        this.register = true;
        this.renderForms();
    },

    swapToLogin: function () {
        this.register = false;
        this.renderForms();
    },

    register: function () {
        var email = this.$el.find('#email'),
            username = this.$el.find('#username').val(),
            password = this.$el.find('#password').val();

        if (!email.is(':valid')) {
            Materialize.toast({html:'<span class="subtitle-lato white-text">Please enter a valid email</span>',displayLength: 5000});

        } else if (password && username) {
            email = email.val();

            $.ajax({
                type: 'POST',
                url: 'auth/register',
                data: {
                    email: email,
                    username: username,
                    password: password
                },
                success: function () {
                    window.location.replace('/');
                },
                error: function (data) {
                    if (data.status === 400) {
                        _.each(data.responseJSON.errors, function(error){
                            Materialize.toast({html:error,displayLength: 5000});
                        });
                    } else if (data.status === 500) {
                        Materialize.toast({html:'Internal Server Error',displayLength: 5000});
                    } else {
                        Materialize.toast({html:data.statusText,displayLength: 5000});
                    }
                }
            });

        } else {
            Materialize.toast({html:'<span class="subtitle-lato white-text">Please fill all the fields</span>',displayLength: 5000});
        }
    }
});

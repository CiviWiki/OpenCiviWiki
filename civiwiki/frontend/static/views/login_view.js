var LoginView = Backbone.View.extend({

    el: '#login',

    initialize: function() {
        this.template = _.template($('#login-template').text());

        this.render();
    },

    render: function() {
        this.$el.html(this.template());

        this.$el.find('#beta-section').hide();

        this.$el.find('.register-slide').hide();
        this.$el.find('#signin-form-button').hide();

        this.$el.find('.datepicker').pickadate({
            selectYears: 116,
            max: new Date(),
            formatSubmit: 'yyyy/mm/dd'
        });
    },

    events: {
        "click #login-button": "logIn",
        "click #open-register-form-button": "openRegisterForm",
        "click #open-login-form-button": "closeRegisterForm",
        "click #register-button": "register"

    },

    logIn: function () {
        var _this = this;

        var username = this.$el.find('#username').val(),
            password = this.$el.find('#password').val();
        if (username && password) {

            $.ajax({
                type: 'POST',
                url: 'api/login',
                data: {
                    username: username,
                    password: password
                },
                success: function (data) {
                      window.location.href = _this.findURLParameter('next');
                },
                error: function (data) {
                  
                  if (data.status === 400) {
                      Materialize.toast(data.statusText, 2000);
                  } else if(data.status === 500 && data.statusText == "inactive account"){
                      window.location.href = "beta";
                  } else {
                    Materialize.toast(data.statusText, 2000);
                  }
                }
            });

        } else {
            Materialize.toast('Please input your email and password!', 3000);
        }
    },

    openRegisterForm: function() {
        this.$el.find(".login-slide").hide();
        this.$el.find(".register-slide").slideDown();
    },

    closeRegisterForm: function() {
        this.$el.find(".register-slide").hide();
        this.$el.find(".login-slide").slideDown();
    },

    register: function () {

        var _this = this;

        var email = this.$el.find('#email').val(),
            username = this.$el.find('#username').val(),
            password = this.$el.find('#password').val(),
            firstName = this.$el.find('#first-name').val(),
            lastName = this.$el.find('#last-name').val(),
            birthday = this.$el.find('#bday').val();

        if (!this.calculateAge(birthday)) {
            Materialize.toast('Must be 13+ to join civiwiki.', 3000);
            return;
        }

        if (email && password && firstName && lastName && username) {

            $.ajax({
                type: 'POST',
                url: 'api/register',
                data: {
                    email: email,
                    username: username,
                    password: password,
                    first_name: firstName,
                    last_name: lastName,
                    birthday: birthday
                },
                success: function (data) {
                    if (data.status_code === 200) {
                        window.location.href = _this.findURLParameter('next');
                        //goes home if no redirect specified else redirects.
                    } else if (data.status_code === 400) {
                      Materialize.toast(data.message, 3000);
                    } else if (data.status_code === 500) {
                        Materialize.toast('Internal Server Error', 3000);
                    }
                },
                error: function(data){
                  console.log(data);
                }
            });

        } else {
            Materialize.toast('Please fill all the fields!', 3000);
        }
    },

    calculateAge: function(birthday) { // birthday is a date
        birthday = new Date(birthday);
        var ageDifMs = Date.now() - birthday.getTime();
        var ageDate = new Date(ageDifMs); // miliseconds from epoch
        return Math.abs(ageDate.getUTCFullYear() - 1970) >= 13;
    },

    findURLParameter: function(val) {
        var result = "/",
            tmp = [];
        location.search
        .substr(1)
            .split("&")
            .forEach(function (item) {
            tmp = item.split("=");
            if (tmp[0] === val) {
                result = decodeURIComponent(tmp[1]);
            }
        });
        return result;
    }

});

var login_view = new LoginView();

var HelloView = Backbone.View.extend({

    el: '#hello',

    initialize: function() {
        this.template = _.template($('#hello-template').text());
        this.$('#bday');
        this.render();
    },

    render: function() {
        this.$el.html(this.template());
    },

    events: {
        "click #log-in-button": "logIn",
        "click #register-button": "register"
    },

    logIn: function () {
        var email = $('#email').val(),
            password = $('#password').val();

        if (email && password) {

            $.ajax({
                type: 'POST',
                url: 'log_in',
                data: {
                    email: email,
                    password: password
                },
                success: function (data) {
                    if (data.data === 'invalid_login') {
                        Materialize.toast('User does not exist!', 3000);
                    } else {
                        window.location.href = 'home';
                    }
                }
            });

        } else {
            Materialize.toast('Please input your email and password!', 3000);
        }
    },

    register: function () {
        var email = $('#email').val(),
            password = $('#password').val(),
            firstName = $('#first-name').val(),
            lastName = $('#last-name').val();
            bday = $('#bday').val();

        if (email && password && firstName && lastName && bday) {
            if(this.calculateAge(bday)<13){
                Materialize.toast("Sorry! You cannot sign up if you are under 13 years old. Please come back when you're of age!", 5000);
            } else{
                $.ajax({
                type: 'POST',
                url: 'register',
                data: {
                    email: email,
                    password: password,
                    first_name: firstName,
                    last_name: lastName
                },
                success: function (data) {
                    if (data.data === 'user_exists_error') {
                        Materialize.toast('We already have a user with this email address!', 3000);
                    } else {
                        window.location.href = 'home';
                    }
                }
            });
            }

        } else {
            Materialize.toast('Please fill all the fields!', 3000);
        }
    },
   
    calculateAge: function(bday){
        var today = new Date(); 
        var day = today.getDate(); 
        var month = today.getMonth()+1; 
        var year = today.getFullYear(); 
        
        var birthday = new Date(bday);
        var bday_year = birthday.getFullYear();
        var bday_month = birthday.getMonth()+1;
        var bday_day = birthday.getDate();

        var age = year - bday_year; 
        if(bday_month > month){
            age--; 
        } 
        else if (bday_month == month && bday_day > day){
            age--;
        }
        return age; 
    }

});

var hello_view = new HelloView();

$('#bday').pickadate({
    selectMonths: true, // Creates a dropdown to control month
    selectYears: 200,  // Creates a dropdown of years to control year
    formatSubmit: 'yyyy-mm-dd',
    hiddenName: true
});

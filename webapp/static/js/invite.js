cw = cw || {};

cw.InviteView = BB.View.extend({

    el: '#invite',

    initialize: function(options) {
        this.options = options || {};
        this.template = _.template($('#invite-template').text());
        this.render();

    },

    render: function() {
        this.$el.html(this.template());

        this.renderInvitees();
    },

    renderInvitees: function() {
        $("#invitee-count").text(this.options.invitees.length);
        _.each(this.options.invitees, function(invitee){
            var item = $('<li class="collection-item"></li>')
            var item_temp = '<div>' + this.options.invitee.email + '</div>';
            if (this.options.invitee.username) {
                item.append('<a href="/profile/' + this.options.invitee.username + '" class="secondary-content">Registered ' + this.options.invitee.date_registered  +'<i class="material-icons">verified_user</i></a>');
            }
            item.append(item_temp);
            $("#invitee-list").append();
        });
    },

    events: {
        'click #send-invites': 'sendInvites',
    },

    sendInvites: function () {
        var emails = this.$el.find('#emails').val();
        var emailList = [];

        if (emails) {
            emailList = emails.split(/\s*[\s,]\s*/);
            var validEmailList = this.validateEmails(emailList);

            if (validEmailList.length != emailList.length) {
                var invalidEmails = _.difference(emailList, validEmailList);
                Materialize.toast("Invalid Emails Present: " + invalidEmails , 5000, 'red');
            } else {
                $.ajax({
                    type: 'POST',
                    url: '/api/invite/',
                    data: {
                        emailList: validEmailList,
                    },
                    success: function (data) {
                        var inviteCount = validEmailList.length;
                        if (data.did_not_invite !== undefined && data.did_not_invite.length > 0) {
                            inviteCount = inviteCount - data.did_not_invite.length;
                            Materialize.toast("Invitation(s) already exist for: " + data.did_not_invite, 5000, 'red');
                        }
                        Materialize.toast(inviteCount + " Invite(s) Sent!", 5000, 'blue');


                        this.$el.find('#emails').val("");
                        this.options.invitees = data.invitees;
                    },
                    error: function (data) {
                        if (data.status === 400 && data.responseJSON) {
                            Materialize.toast(data.responseJSON.message, 5000, 'red');
                        } else {
                            Materialize.toast(data.statusText, 5000, 'red');
                        }
                    }
                }, this);
            }


        } else {
            Materialize.toast("<span class=\"subtitle-lato white-text\">Put some emails in!</span>", 5000);
        }
    },

    validateEmails: function (emailList) {
        var emailRegex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;

        newList = _.filter(emailList, function(email){
            return emailRegex.test(email);
        }, this);

        return newList;
   },

});

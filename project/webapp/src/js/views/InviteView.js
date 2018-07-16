
import { View } from 'backbone.marionette';

cw.InviteView = View.extend({
//   el: '#invite',

  initialize(options) {
    this.options = options || {};
    this.template = _.template($('#invite-template').text());
    this.singleInviteTemplate = _.template($('#single-invite-template').text());
    this.render();
  },

  render() {
    this.$el.html(this.template());

    this.renderInvitees();
  },

  renderInvitees() {
    this.$('#invitee-count').text(this.options.invitees.length);
    this.$('#invitee-list').empty();
    _.each(
      this.options.invitees,
      function (invitee) {
        // invitee.date_invited = this.time_ago(new Date(Date.now() -  new Date(invitee.date_invited).getTime()));
        invitee.date_invited = new Date(invitee.date_invited);
        $('#invitee-list').append(this.singleInviteTemplate(invitee));
      },
      this,
    );
  },

  events: {
    'click #send-invites': 'sendInvites',
  },

  sendInvites() {
    const _this = this;
    const emails = this.$('#emails')
      .val()
      .trim();
    const custom_message = this.$('#custom_message')
      .val()
      .trim();
    let emailList = [];

    if (emails) {
      emailList = emails.split(/\s*[\s,]\s*/);
      const validEmailList = this.validateEmails(emailList);

      if (validEmailList.length != emailList.length) {
        const invalidEmails = _.difference(emailList, validEmailList);
        Materialize.toast(`Invalid Emails Present: ${invalidEmails}`, 5000, 'red');
      } else {
        $.ajax({
          type: 'POST',
          url: '/api/invite/',
          data: {
            emailList: validEmailList,
            custom_message,
          },
          success(data) {
            let inviteCount = validEmailList.length;
            if (data.did_not_invite !== undefined && data.did_not_invite.length > 0) {
              inviteCount -= data.did_not_invite.length;
              Materialize.toast(
                `Invitation(s) already exist for: ${data.did_not_invite}`,
                5000,
                'red',
              );
            }
            Materialize.toast(`${inviteCount} Invite(s) Sent!`, 5000, 'blue');

            _this.$('#emails').val('');
            _this.$('#custom_message').val('');
            _this.options.invitees = data.invitees;
            _this.renderInvitees();
          },
          error(data) {
            if (data.status === 400 && data.responseJSON) {
              Materialize.toast(data.responseJSON.message, 5000, 'red');
            } else {
              Materialize.toast(data.statusText, 5000, 'red');
            }
          },
        });
      }
    } else {
      Materialize.toast('<span class="subtitle-lato white-text">Put some emails in!</span>', 5000);
    }
  },

  validateEmails(emailList) {
    const emailRegex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;

    newList = _.filter(
      emailList,
      email => emailRegex.test(email),
      this,
    );

    return newList;
  },

  time_ago(time) {
    switch (typeof time) {
      case 'number':
        break;
      case 'string':
        time = +new Date(time);
        break;
      case 'object':
        if (time.constructor === Date) time = time.getTime();
        break;
      default:
        time = +new Date();
    }

    const time_formats = [
      [60, 'seconds', 1], // 60
      [120, '1 minute ago', '1 minute from now'], // 60*2
      [3600, 'minutes', 60], // 60*60, 60
      [7200, '1 hour ago', '1 hour from now'], // 60*60*2
      [86400, 'hours', 3600], // 60*60*24, 60*60
      [172800, 'Yesterday', 'Tomorrow'], // 60*60*24*2
      [604800, 'days', 86400], // 60*60*24*7, 60*60*24
      [1209600, 'Last week', 'Next week'], // 60*60*24*7*4*2
      [2419200, 'weeks', 604800], // 60*60*24*7*4, 60*60*24*7
      [4838400, 'Last month', 'Next month'], // 60*60*24*7*4*2
      [29030400, 'months', 2419200], // 60*60*24*7*4*12, 60*60*24*7*4
      [58060800, 'Last year', 'Next year'], // 60*60*24*7*4*12*2
      [2903040000, 'years', 29030400], // 60*60*24*7*4*12*100, 60*60*24*7*4*12
    ];
    let seconds = (+new Date() - time) / 1000;


    let token = 'ago';


    let list_choice = 1;

    if (seconds === 0) {
      return 'Just now';
    }
    if (seconds < 0) {
      seconds = Math.abs(seconds);
      token = 'from now';
      list_choice = 2;
    }
    let i = 0;


    let format;
    while ((format = time_formats[i++])) {
      if (seconds < format[0]) {
        if (typeof format[2] === 'string') return format[list_choice];
        return `${Math.floor(seconds / format[2])} ${format[1]} ${token}`;
      }
    }

    return time;
  },
});

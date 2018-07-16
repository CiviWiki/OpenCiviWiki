import { View } from 'backbone.marionette';
import baseTemplate from 'Templates/layouts/invite.html';
import singleInviteTemplate from 'Templates/components/Invite/single_invite.html';

const InviteView = View.extend({
  template: baseTemplate,

  initialize() {
    this.invitees = this.getOption('context').data;
  },

  renderInvitees() {
    const view = this;
    view.$('#invitee-count').text(this.invitees.length);
    view.$('#invitee-list').empty();
    _.each(view.invitees, (invitee) => {
      $('#invitee-list').append(singleInviteTemplate(invitee));
    });
  },

  events: {
    'click #send-invites': 'sendInvites',
  },

  sendInvites() {
    const view = this;
    const emails = this.$('#emails')
      .val()
      .trim();
    const customMessage = this.$('#custom_message')
      .val()
      .trim();
    let emailList = [];

    if (emails) {
      emailList = emails.split(/\s*[\s,]\s*/);
      const validEmailList = this.validateEmails(emailList);

      if (validEmailList.length !== emailList.length) {
        const invalidEmails = _.difference(emailList, validEmailList);
        M.toast({ html: `Invalid Emails Present: ${invalidEmails}`, classes: 'red' });
      } else {
        $.ajax({
          type: 'POST',
          url: '/api/invite/',
          data: {
            emailList: validEmailList,
            customMessage,
          },
          success(data) {
            let inviteCount = validEmailList.length;
            if (data.did_not_invite !== undefined && data.did_not_invite.length > 0) {
              inviteCount -= data.did_not_invite.length;
              M.toast({
                html: `Invitation(s) already exist for: ${data.did_not_invite}`,
                classes: 'red',
              });
            }
            M.toast({ html: `${inviteCount} Invite(s) Sent!`, classes: 'blue' });

            view.$('#emails').val('');
            view.$('#custom_message').val('');
            view.invitees = data.invitees;
            view.renderInvitees();
          },
          error(data) {
            if (data.status === 400 && data.responseJSON) {
              M.toast({ html: data.responseJSON.message, classes: 'red' });
            } else {
              M.toast({ html: data.statusText, classes: 'red' });
            }
          },
        });
      }
    } else {
      M.toast({ html: '<span class="subtitle-lato white-text">Put some emails in!</span>' });
    }
  },

  validateEmails(emailList) {
    const emailRegex = /^([a-zA-Z0-9_.+-])+@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    const newList = _.filter(emailList, email => emailRegex.test(email), this);
    return newList;
  },
});
export default InviteView;

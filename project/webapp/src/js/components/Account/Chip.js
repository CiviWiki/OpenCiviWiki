import { View } from 'backbone.marionette';
import chipTemplate from 'Templates/components/Account/chip.html';

const AccountChip = View.extend({
  tagName: 'div',
  className: 'col s12 m6',
  template: chipTemplate,
});

export default AccountChip;

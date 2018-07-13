import { View } from 'backbone.marionette';
import civiTemplate from 'Templates/components/Profile/civi.html';

const ProfileCivi = View.extend({
  tagName: 'div',
  className: 'ProfileCivi civi-card white',
  template: civiTemplate,
});

export default ProfileCivi;

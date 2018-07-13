import { View } from 'backbone.marionette';
import repTemplate from 'Templates/components/Profile/representative.html';

const Representative = View.extend({
  tagName: 'div',
  className: 'ProfileIssue',
  template: repTemplate,
});

export default Representative;

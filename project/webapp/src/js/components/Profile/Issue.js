import { View } from 'backbone.marionette';
import issueTemplate from 'Templates/components/Profile/issue.html';

const ProfileIssue = View.extend({
  tagName: 'div',
  className: 'ProfileIssue',
  template: issueTemplate,
});

export default ProfileIssue;

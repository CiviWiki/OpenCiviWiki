import { View } from 'backbone.marionette';
import threadOutlineTemplate from 'Templates/components/Thread/thread_outline.html';

const ThreadOutlineView = View.extend({
  tagName: 'div',
  className: 'thread-outline',
  template: threadOutlineTemplate,
});

export default ThreadOutlineView;

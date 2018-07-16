import { View } from 'backbone.marionette';
import threadBodyTemplate from 'Templates/components/Thread/thread_body.html';

const ThreadBodyView = View.extend({
  tagName: 'div',
  className: 'thread-body',
  template: threadBodyTemplate,
});

export default ThreadBodyView;

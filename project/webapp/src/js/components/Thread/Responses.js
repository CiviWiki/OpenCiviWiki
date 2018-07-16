import { View } from 'backbone.marionette';
import threadResponseTemplate from 'Templates/components/Thread/thread_responses.html';

const ResponsesView = View.extend({
  tagName: 'div',
  className: 'thread-reponses',
  template: threadResponseTemplate,
});

export default ResponsesView;

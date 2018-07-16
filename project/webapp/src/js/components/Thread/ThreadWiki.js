import { View } from 'backbone.marionette';
import threadWikiTemplate from 'Templates/components/Thread/thread_wiki.html';

const ThreadWikiView = View.extend({
  tagName: 'div',
  className: 'thread-wiki',
  template: threadWikiTemplate,
});

export default ThreadWikiView;

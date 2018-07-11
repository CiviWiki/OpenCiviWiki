import { View } from 'backbone.marionette';
import emptyTemplate from 'templates/components/Thread/empty.html';

const EmptyView = View.extend({
  tagName: 'div',
  className: 'section',
  template: emptyTemplate,
});

export default EmptyView;

import { View } from 'backbone.marionette';
import emptyTemplate from 'Templates/components/common/empty.html';

const EmptyView = View.extend({
  template: emptyTemplate,
});

export default EmptyView;

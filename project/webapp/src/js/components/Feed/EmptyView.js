import { View } from "backbone.marionette"
import emptyTemplate from "templates/components/Thread/empty.html";

var EmptyView = View.extend({
  template: emptyTemplate,
});

export default EmptyView;

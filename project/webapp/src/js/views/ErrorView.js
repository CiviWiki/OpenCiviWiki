import { View } from 'backbone.marionette';
import errorTemplate from 'Templates/common/error.html';

const ErrorView = View.extend({
  tagName: 'div',
  className: 'error-container',
  template: errorTemplate,
});

export default ErrorView;

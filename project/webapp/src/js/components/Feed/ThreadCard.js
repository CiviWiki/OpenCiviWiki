import { View } from 'backbone.marionette';
import cardTemplate from 'Templates/components/Thread/card.html';

const ThreadCard = View.extend({
  tagName: 'div',
  className: 'ThreadCard col s12',
  template: cardTemplate,
});

export default ThreadCard;

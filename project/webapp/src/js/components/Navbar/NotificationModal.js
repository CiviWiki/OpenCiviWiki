import { View, CollectionView } from 'backbone.marionette';

import baseTemplate from 'Templates/components/Notification/modal.html';
import itemTemplate from 'Templates/components/Notification/item.html';
import EmptyView from '../EmptyView';

const NotificationItemView = View.extend({
  template: itemTemplate,
});

const NotificationCollectionView = CollectionView.extend({
  childView: NotificationItemView,

  emptyView: EmptyView,

  isEmpty() {
    return this.collection.length === 0;
  },
});

const NotificationModal = View.extend({
  template: baseTemplate,

  regions: {
    notificationsList: '#notification-items',
  },

  initialize() {
    this.notifications = this.getOption('notifications');
  },

  onRender() {
    this.showChildView(
      'notificationsList',
      new NotificationCollectionView({ collection: this.notifications }),
    );
  },
});

export default NotificationModal;

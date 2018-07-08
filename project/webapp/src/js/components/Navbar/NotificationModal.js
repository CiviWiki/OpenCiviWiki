import { View, CollectionView } from "backbone.marionette";

import EmptyView from "../EmptyView";

import baseTemplate from "templates/components/Notification/modal.html";
import itemTemplate from "templates/components/Notification/item.html";

const NotificationItemView = View.extend({
  template: itemTemplate
});

const NotificationCollectionView = CollectionView.extend({
  childView: NotificationItemView,

  emptyView: EmptyView,

  isEmpty: function(options) {
    return this.collection.length == 0;
  }
});

const NotificationModal = View.extend({
  template: baseTemplate,

  regions: {
    notificationsList: "#notification-items"
  },

  initialize() {
    this.notifications = this.getOption("notifications");
  },

  onRender() {
    this.showChildView(
      "notificationsList",
      new NotificationCollectionView({ collection: this.notifications })
    );
  }
});

export default NotificationModal;

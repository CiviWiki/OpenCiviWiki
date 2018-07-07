import { View, CollectionView } from "backbone.marionette";

import Notifications from "../../collections/Notifications";
import EmptyView from "../EmptyView";

import baseTemplate from "templates/components/Notifications/modal.html";
import itemTemplate from "templates/components/Notifications/item.html";

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
    this.initialNotificationShown = false;
    this.notified = false;

    this.unreadNotifications = new Notifications();
    this.unreadNotifications.fetchNotifications();
  },

  onRender() {
    this.showChildView(
      "notificationsList",
      new NotificationCollectionView({ collection: this.unreadNotifications })
    );

    let unreadCount = this.unreadNotifications.length;
    if (unreadCount === 0) {
      $("#notify-count-wrapper").addClass("hide");
      $("#notify-icon")
        .html("notifications_none")
        .removeClass("active");
    } else {
      $("#notify-count-wrapper").removeClass("hide");
      $("#notify-icon")
        .html("notifications")
        .addClass("active");
    }

    if (unreadCount > 5 && !this.initialNotificationShown) {
      Materialize.toast("You have " + unreadCount + " new notifications", 5000);
      this.initialNotificationShown = true;
      this.notified = true;
    }
  }
});

export default NotificationModal;
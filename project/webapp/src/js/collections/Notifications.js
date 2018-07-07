import { Collection } from "backbone";
import { Notification } from "../models";

const Notifications = Collection.extend({
  model: Notification,
  url: "/inbox/notifications/api",

  initialize() {
    this.consecutive_misfires = 0;
    this.notify_badge_class = "#live_notify_badge";
  },

  fetchNotifications() {
    _.delay(this.fetchApiData, 1000, this);
  },

  fetchApiData(collection) {
    let query = {
      max: 99
    };

    $.ajax({
      url: `${collection.url}/unread_list/`,
      type: "GET",
      data: query,
      success: function(data) {
        collection.consecutive_misfires = 0;

        if (data.unread_count > 0) {
          collection.reset(data.unread_list);
        }

        _.each(data.unread_list, function(notifications) {
          var old_notification = _.findWhere(collection.models, {id: notifications.id});
          // var json_Data = JSON.parse(notifications.data);
          if (!old_notification) {
            if (json_Data !== null) {
              Materialize.toast(notifications.data.popup_string, 5000);
            } else {
              Materialize.toast("You have a new notification", 5000);
            }
          }
        });
      },
      error: function() {
        collection.consecutive_misfires++;
      }
    });

    if (collection.consecutive_misfires < 10) {
      _.delay(collection.fetchApiData, 30000, collection);
    } else {
      collection.collection.trigger("selected", collection.model);
      let badge = $(collection.notify_badge_class);
      badge.html("!");
      badge.attr("title", "Connection lost!");
    }
  }
});

export default Notifications;

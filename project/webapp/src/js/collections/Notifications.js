import { Collection } from "backbone";
import { Notification } from "../models";

const Notifications = Collection.extend({
  model: Notification,
  url: "/inbox/notifications/api",

  initialize() {
    this.consecutive_misfires = 0;
    this.initialNotificationShown = false;
    this.newIds = [];
  },

  startFetchPoll() {
    _.delay(this.fetchUnread, 1000, this);
  },

  fetchUnread(collection) {
    const query = { max: 99 };
    $.ajax({
      url: `${collection.url}/unread_list/`,
      type: "GET",
      data: query,
      success: data => {
        collection.consecutive_misfires = 0;
        if (data.unread_count > 0) {
          collection.newIds = this.findNewIds(collection.models, data.unread_list);
          if (collection.newIds.length > 0) collection.reset(data.unread_list);
        }
      },
      error: () => { collection.consecutive_misfires++; },
      complete: () => {
        // Checking if polling should be continued
        if (collection.consecutive_misfires < 10) {
          _.delay(collection.fetchUnread, 3000, collection);
        } else {
          this.trigger("error");
        }
      }
    });
  },

  findNewIds(oldUnreadList, newUnreadList) {
    // Compare the current collection to the new and return the ids of the difference
    const newIds = [];
    _.each(newUnreadList, unreadItem => {
      unreadItem.data = JSON.parse(unreadItem.data);
      const itemIsOld = _.findWhere(oldUnreadList, { id: unreadItem.id });
      if (!itemIsOld) {
        newIds.push(unreadItem.id);
      }
    });
    return newIds;
  }
});

export default Notifications;

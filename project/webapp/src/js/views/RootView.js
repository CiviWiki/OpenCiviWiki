import { View } from "backbone.marionette";

import { Account } from "../models";
import { Notifications } from "../collections";

import Navbar from "../components/Navbar/Navbar";
import NotificationModal from "../components/Navbar/NotificationModal";
import rootTemplate from "templates/layouts/root.html";

import "materialize-css/dist/css/materialize.css";
import "styles/base.less";

const RootView = View.extend({
  tagName: "div",
  className: "RootView",
  template: rootTemplate,

  regions: {
    navbar: ".main-navbar",
    content: ".main-content",
    notificationModal: "#notifications-modal"
  },

  ui: {
    modal: ".modal",
    modalHolder: "#item-notifications"
  },

  childViewEvents: {
    "click:notifyIcon": "showNotificationModal"
  },

  initialize() {
    this.currentUser = new Account({
      username: this.getOption("context").username
    });
    this.notifications = new Notifications();

    this.currentUser.fetch();
    this.notifications.startFetchPoll();
  },

  onRender() {
    this.showChildView("navbar", new Navbar({ model: this.currentUser, notifications: this.notifications  }));
    this.showChildView("notificationModal", new NotificationModal({ notifications: this.notifications }));

    M.Modal.init(this.getUI("modal"));
  },

  showNotificationModal() {
    M.Modal.getInstance(this.getUI("modal")).open();
  },

  renderContent(contentView) {
    this.showChildView("content", contentView);
  }
});

export default RootView;

import { View } from "backbone.marionette";

import Navbar from "../components/Navbar/Navbar";
import NotificationModal from "../components/Navbar/NotificationModal";
import rootTemplate from "templates/layouts/root.html";

import "materialize-css/dist/css/materialize.css";
import "styles/base.less";

const RootView = View.extend({
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
    this.currentUser = this.getOption("account"); 
    this.notifications = this.getOption("notifications"); 
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

import { View } from "backbone.marionette";
import { Account } from "../models";
// import rootTemplate from 'templates/'
import Navbar from "../components/Navbar/Navbar";
import NotificationModal from "../components/Navbar/NotificationModal";
import rootTemplate from "templates/layouts/root.html";

const RootLayout = View.extend({
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
  },

  onRender() {
    this.showChildView("navbar", new Navbar({ model: this.currentUser }));
    this.showChildView("notificationModal", new NotificationModal());

    M.Modal.init(this.getUI("modal"));
  },

  showNotificationModal() {
    M.Modal.getInstance(this.getUI("modal")).open();
  },

  renderContent(contentView) {
    this.showChildView("content", contentView);
  }
});

export default RootLayout;

import { View } from 'backbone.marionette';
import navbarTemplate from 'templates/components/common/navbar.html';

import 'styles/navbar.less';
import 'styles/utils.less';

const Navbar = View.extend({
  tagName: 'div',
  className: 'nav-wrapper',
  template: navbarTemplate,

  ui: {
    button: '#js-toggle-menu',
    dropdown: '#js-dropdown-menu',
    dropdownIcon: '.js-dropdown-icon',
    notificationButton: '#item-notifications',
    notificationBadge: '#notify-count-wrapper',
    notificationIcon: '#notify-icon',
    notificationCount: '#live_notify_badge',
  },

  events: {
    'click @ui.button': 'toggleDropdown',
    'click @ui.notificationButton': 'markNotifications',
  },

  modelEvents: {
    change: 'render',
  },

  initialize() {
    this.notifications = this.getOption('notifications');
    this.listenTo(this.notifications, 'reset', this.onNotification);
    this.listenTo(this.notifications, 'error', this.onNotificationError);
  },

  onNotification() {
    this.renderNotificationToast();
    this.renderNotificationBadge();
  },

  onNotificationError() {
    this.getUI('notificationCount')
      .html('!')
      .attr('title', 'Connection lost!');
  },

  toggleDropdown(toggleEvent) {
    // Open the dropdown menu
    toggleEvent.stopPropagation();
    this.getUI('dropdown').toggleClass('hide');
    this.getUI('dropdownIcon').toggleClass('hide');

    // Detect clicking outside of dropdown to close it
    const view = this;
    $(document).on('click', (event) => {
      const $target = $(event.target);

      if ($target.parents('#js-dropdown-menu').length === 0) {
        view.getUI('dropdown').addClass('hide');
        view.getUI('dropdownIcon').toggleClass('hide');
        $(this).unbind(event);
      }
    });
  },

  markNotifications() {
    // Send a request to the server marking that the notifications have been read
    this.triggerMethod('click:notifyIcon', this);

    const view = this;
    $.ajax({
      type: 'GET',
      url: '/inbox/notifications/mark-all-as-read/',
      success: () => {
        // Remove the notification count badge
        view.getUI('notificationBadge').addClass('hide');
        view
          .getUI('notificationIcon')
          .html('notifications_none')
          .removeClass('active');
      },
      error: () => {
        view.onNotificationError();
      },
    });
  },

  renderNotificationToast() {
    // Shows the Toast message based on the number of notifications
    if (this.notifications.length <= 0) return;
    if (this.notifications.length === 1) {
      M.toast({ html: this.notifications.at(0).get('data').popup_string });
    } else if (!this.notifications.initialNotificationShown) {
      this.notifications.initialNotificationShown = true;
      M.toast({
        html: `You have ${this.notifications.length} new notifications`,
      });
    } else {
      _.each(this.notifications.newIds, (id) => {
        M.toast({
          html: this.notifications.get(id).get('data').popup_string,
        });
      });
    }
  },

  renderNotificationBadge() {
    // Show and hide the number by the notification icon
    if (this.notifications.length === 0) {
      this.getUI('notificationBadge').addClass('hide');
      this.getUI('notificationIcon')
        .html('notifications_none')
        .removeClass('active');
    } else {
      this.getUI('notificationCount').html(this.notifications.length);
      this.getUI('notificationBadge').removeClass('hide');
      this.getUI('notificationIcon')
        .html('notifications')
        .addClass('active');
    }
  },
});

export default Navbar;

import { View } from "backbone.marionette";
import navbarTemplate from "templates/components/common/navbar.html";

const Navbar = View.extend({
  template: navbarTemplate,

  ui: {
    button: "#js-toggle-menu",
    dropdown: "#js-dropdown-menu",
    dropdownIcon: ".js-dropdown-icon",
    notificationButton: "#item-notifications",
    notificationCount: "#notify-count-wrapper",
    notificationIcon: "#notify-icon"
  },

  events: {
    "click @ui.button": "toggleDropdown",
    "click @ui.notificationButton": "markNotifications"
  },

  modelEvents: {
    'change': 'render'
  },

  toggleDropdown(event){
    // Open the dropdown menu
    event.stopPropagation();
    this.getUI("dropdown").toggleClass("hide");
    this.getUI("dropdownIcon").toggleClass("hide");

    // Detect clicking outside of dropdown to close it
    let _this = this;
    $(document).on("click", function(event) {
      let $target = $(event.target);

      if ($target.parents("#js-dropdown-menu").length == 0) {
        _this.getUI("dropdown").addClass("hide");
        _this.getUI("dropdownIcon").toggleClass("hide");
        $(this).unbind(event);
      }
    });
  },
  
  markNotifications(){
    console.log(this.model);
    this.triggerMethod('click:notifyIcon', this);

    let _this = this;
    $.ajax({
      type: "GET",
      url: "/inbox/notifications/mark-all-as-read/",
      success: function() {
        _this.getUI("notificationCount").addClass("hide");
        _this.getUI("notificationIcon")
          .html("notifications_none")
          .removeClass("active");
      }
    });
  }
});

export default Navbar;

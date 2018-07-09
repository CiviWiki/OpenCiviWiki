import { View, CollectionView } from "backbone.marionette";

import EmptyView from "../EmptyView";

import baseTemplate from "templates/components/Feed/category_navbar.html";
import itemTemplate from "templates/components/Feed/category_item.html";

const dropdownButton = `
<li class="dropdown-wrapper">
<a class="dropdown-button category-item" data-id="arrow" data-activates="categories-dropdown">
<i class="material-icons">arrow_drop_down</i>
</a>
</li>
`;
const CategoryNavbarItemView = View.extend({
  tagName: "li",
  className: "user-categories",
  template: itemTemplate,

  ui: {
    item: ".category-item"
  },
  // events: {
  //     'click a': 'itemSelected'
  // },
  triggers: {
    "click a": "select:item",
  }

  //   itemSelected(event) {
  //     event.target.addClass('active');
  //     this.triggerMethod("select:item", this);
  //   }
});

const CategoryNavbarCollectionView = CollectionView.extend({
  childView: CategoryNavbarItemView,

  childViewEvents: {
    "select:item": "itemSelected"
  },

  emptyView: EmptyView,

  isEmpty: function(options) {
    return this.collection.length == 0;
  },
  initialize() {
    this.activeCategory = -1;
    $(window).on("resize", this.updatePriorityNav.bind(this));
  },
  onRender() {
    this.updatePriorityNav();
  },
  filter: function(child) {
    return child.get("preferred");
  },

  itemSelected(childView) {
    this.$(".category-item").removeClass("active");
    childView.getUI("item").addClass("active");

    if (this.activeCategory != childView.model.get("id")) {
      this.activeCategory = childView.model.get("id");
      this.triggerMethod("click:categoryItem", this);
    }
  },

  updatePriorityNav: function() {
    var dropdown = this.$("#categories-dropdown");
    var navWidth =
      $("#user-categories-list > li.dropdown-wrapper").width() +
      $("#user-categories-list > li.category-all").width();
    var containerWidth = $(".nav-categories").width();

    $("#user-categories-list > li.user-categories").each(function() {
      navWidth += $(this).width();
    });

    if (navWidth > containerWidth) {
      var lastItem = $(
        "#user-categories-list > li.user-categories"
      ).last();
      if (lastItem.text()) {
        lastItem.attr("data-width", lastItem.width());
        dropdown.prepend(lastItem);
        this.updatePriorityNav();
      }
    } else {
      var firstDropdownElement = dropdown.children().first();
      if (navWidth + firstDropdownElement.data("width") < containerWidth) {
        firstDropdownElement.insertBefore(
          $("#user-categories-list > li.dropdown-wrapper")
        );
      }
    }
  }
});

const CategoryNavbar = View.extend({
  template: baseTemplate,

  regions: {
    userCategories: "#user-categories-list"
  },

  ui: {
    userCategories: "#user-categories-list",
    dropdownButton: ".dropdown-button",
    categoryManageButton: ".category-button"
  },

  childViewEvents: {
    "click:categoryItem": "triggerToParent"
  },

  triggers: {
    "click @ui.categoryManageButton": "click:categoryManageButton",
  },

  initialize() {
    this.categories = this.getOption("categories");
    this.activeCategory = -1;
  },

  triggerToParent(childView) {
    this.activeCategory = childView.activeCategory;
    this.triggerMethod("click:categoryItem", this);
  },

  onRender() {
    this.showChildView(
      "userCategories",
      new CategoryNavbarCollectionView({ collection: this.categories })
    );
    this.getUI("userCategories").append(dropdownButton);

    M.Dropdown.init(this.getUI("dropdownButton"), {
      coverTrigger: false,
      constrainWidth: false,
      hover: true
    });
  }
});

export default CategoryNavbar;

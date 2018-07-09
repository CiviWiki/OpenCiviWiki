import { View, CollectionView } from "backbone.marionette";

import baseTemplate from "templates/components/Category/modal.html";
import itemTemplate from "templates/components/Category/input_checkbox.html";

const EditCategoryItemView = View.extend({
  tagName: "p",
  className: "col s12 m6 category-checkbox",
  template: itemTemplate
});

const EditCategoryCollectionView = CollectionView.extend({
  tagName: "div",
  className: "row",
  childView: EditCategoryItemView
});

const EditCategoryModal = View.extend({
  template: baseTemplate,

  regions: {
    userCategoryList: "#user-category-form"
  },

  ui: {
    categoryModal: ".categories-modal"
  },

  initialize() {
    this.categories = this.getOption("categories");
  },

  onRender() {
    this.showChildView(
      "userCategoryList",
      new EditCategoryCollectionView({ collection: this.categories })
    );

    M.Modal.init(this.getUI("categoryModal"));
    this.markUserCategories();
  },

  openModal() {
    M.Modal.getInstance(this.getUI("categoryModal")).open();
  },

  markUserCategories() {}
});

export default EditCategoryModal;

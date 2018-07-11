import { View, CollectionView } from 'backbone.marionette';

import baseTemplate from 'Templates/components/Category/modal.html';
import itemTemplate from 'Templates/components/Category/input_checkbox.html';

const EditCategoryItemView = View.extend({
  tagName: 'p',
  className: 'col s12 m6 category-checkbox',
  template: itemTemplate,

  ui: {
    input: 'input',
  },
});

const EditCategoryCollectionView = CollectionView.extend({
  tagName: 'div',
  className: 'row',
  childView: EditCategoryItemView,
});

const EditCategoryModal = View.extend({
  template: baseTemplate,

  regions: {
    userCategoryList: '#user-category-form',
  },

  ui: {
    categoryModal: '.categories-modal',
    modalSaveButton: '.change-category',
  },

  events: {
    'click @ui.modalSaveButton': 'updatePreferredCategories',
  },

  initialize() {
    this.categories = this.getOption('categories');
  },

  onRender() {
    this.showChildView(
      'userCategoryList',
      new EditCategoryCollectionView({ collection: this.categories }),
    );

    M.Modal.init(this.getUI('categoryModal'));
    this.modal = M.Modal.getInstance(this.getUI('categoryModal'));
  },

  openModal() {
    this.modal.open();
  },
  closeModal() {
    this.modal.close();
  },

  updatePreferredCategories() {
    const view = this;

    const selectedCategories = [];

    const checkboxes = view.getChildView('userCategoryList').$('input:checked');
    _.each(checkboxes, (checkbox) => {
      selectedCategories.push($(checkbox).val());
    });

    if (selectedCategories.length > 0) {
      $.ajax({
        url: '/api/edit_user_categories/',
        type: 'POST',
        data: {
          'categories[]': selectedCategories,
        },
        success() {
          M.toast({ html: 'Categories Changed' });
          view.categories.fetch();
          view.closeModal();
        },
      });
    } else {
      M.toast({ html: 'Please select at least one category' });
    }
  },
});

export default EditCategoryModal;

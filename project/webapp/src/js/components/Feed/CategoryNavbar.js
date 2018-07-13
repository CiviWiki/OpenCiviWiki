import { View, CollectionView } from 'backbone.marionette';

import baseTemplate from 'Templates/components/Feed/category_navbar.html';
import itemTemplate from 'Templates/components/Feed/category_item.html';

import EmptyView from '../EmptyView';

const CategoryNavbarItemView = View.extend({
  tagName: 'li',
  className: 'user-categories',
  template: itemTemplate,

  ui: {
    item: '.category-item',
  },

  triggers: {
    'click a': 'select:item',
  },
});

const CategoryNavbarCollectionView = CollectionView.extend({
  childView: CategoryNavbarItemView,

  childViewEvents: {
    'select:item': 'itemSelected',
  },

  emptyView: EmptyView,

  isEmpty() {
    return this.collection.length === 0;
  },
  filter: child => child.get('preferred'),
  initialize() {
    this.activeCategory = -1;
  },

  itemSelected(childView) {
    this.$('.category-item').removeClass('active');
    childView.getUI('item').addClass('active');

    if (this.activeCategory !== childView.model.get('id')) {
      this.activeCategory = childView.model.get('id');
      this.triggerMethod('click:categoryItem', this);
    }
  },
});

const CategoryNavbar = View.extend({
  template: baseTemplate,

  regions: {
    userCategories: '#user-categories-list',
  },

  ui: {
    userCategories: '#user-categories-list',
    categoryManageButton: '.category-button',
  },

  childViewEvents: {
    'click:categoryItem': 'triggerToParent',
  },

  triggers: {
    'click @ui.categoryManageButton': 'click:categoryManageButton',
  },

  initialize() {
    this.categories = this.getOption('categories');
    this.activeCategory = -1;
  },

  triggerToParent(childView) {
    this.activeCategory = childView.activeCategory;
    this.triggerMethod('click:categoryItem', this);
  },

  onRender() {
    this.showChildView(
      'userCategories',
      new CategoryNavbarCollectionView({ collection: this.categories }),
    );
  },
});

export default CategoryNavbar;

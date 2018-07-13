import { View } from 'backbone.marionette';

import threadlistTemplate from 'templates/components/Profile/tab.html';
import ItemCollectionView from './ItemCollectionView';
import EmptyView from '../EmptyView';

const TabView = View.extend({
  tagName: 'div',
  className: 'Tab',
  template: threadlistTemplate,

  regions: {
    list: '#tab-list',
  },

  templateContext() {
    // Render title if present
    const context = {};
    if (this.title) {
      context.title = this.title;
    } else {
      context.title = '';
    }
    return context;
  },

  initialize() {
    this.collection = this.getOption('collection');
    this.collectionChildView = this.getOption('collectionChildView');
    this.title = this.getOption('title', '');
  },

  onRender() {
    this.renderTab();
  },

  renderTab() {
    const options = { collection: this.collection, childView: this.collectionChildView };
    if (this.emptyView) {
      options.emptyView = this.emptyView;
    } else {
      options.emptyView = EmptyView;
    }
    this.showChildView('list', new ItemCollectionView(options));
  },
});

export default TabView;

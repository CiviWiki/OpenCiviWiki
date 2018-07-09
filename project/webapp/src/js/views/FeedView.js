import { View } from 'backbone.marionette';

import feedTemplate from 'templates/layouts/feed.html';
import emptyTemplate from 'templates/components/Thread/empty.html';
import 'styles/feed.less';

import { Threads, Categories } from '../collections';
import EditCategoryModal from '../components/Feed/EditCategoryModal';
import CategoryNavbar from '../components/Feed/CategoryNavbar';
import ThreadCollectionView from '../components/Feed/ThreadCollectionView';
import ThreadList from '../components/Feed/ThreadList';
import ThreadLink from '../components/Thread/Link';

const EmptyView = View.extend({
  template: emptyTemplate,
});

const FeedView = View.extend({
  tagName: 'div',
  className: 'FeedView',
  id: 'feed',
  template: feedTemplate,

  regions: {
    categoryModal: '.categories-modal-holder',
    newThreadModal: '.new-thread-modal-holder',
    categoryNavbar: '.navbar-container',
    trending: '#trending-list',
    feed: '#feed-list',
    drafts: '#drafts-list',
  },

  ui: {
    scrollElement: '.scroll-col',
  },

  childViewEvents: {
    'click:categoryItem': 'filterFeed',
    'click:categoryManageButton': 'showCategoryModal',
  },

  initialize() {
    this.threads = new Threads();
    this.draftThreads = new Threads();
    this.topThreads = new Threads();
    this.categories = new Categories();
    this.navCategories = new Categories();

    this.listenTo(this.categories, 'reset', this.fillNavCategories);
  },

  onRender() {
    // Navbar for filtering by category
    this.showChildView('categoryNavbar', new CategoryNavbar({ categories: this.navCategories }));
    // Modal for choosing preferred categories
    this.showChildView('categoryModal', new EditCategoryModal({ categories: this.categories }));
    this.categories.fetch({ reset: true });

    // Main Feed
    this.showChildView(
      'feed',
      new ThreadList({
        threads: this.threads,
        emptyView: EmptyView,
      }),
    );
    this.getUI('scrollElement').height($(window).height() - $('nav').height());
    this.threads.fetchAll();

    // Draft Threads
    this.showChildView(
      'drafts',
      new ThreadList({
        threads: this.draftThreads,
        title: 'drafts',
      }),
    );
    this.draftThreads.fetchDrafts();

    // "Trending" threads
    this.showChildView(
      'trending',
      new ThreadCollectionView({
        collection: this.topThreads,
        childView: ThreadLink,
      }),
    );
    this.topThreads.fetchTop();
  },

  fillNavCategories() {
    this.navCategories.reset(this.categories.models);
    this.navCategories.add({ name: 'All', id: '-1', preferred: true });
  },

  filterFeed(childView) {
    if (childView.activeCategory === -1) {
      this.threads.fetch({ reset: true });
    } else {
      this.threads.fetch({
        data: { category_id: childView.activeCategory },
        reset: true,
      });
    }
  },

  showCategoryModal() {
    this.getChildView('categoryModal').openModal();
  },
});

export default FeedView;

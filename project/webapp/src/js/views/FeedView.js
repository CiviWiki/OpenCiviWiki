import { View } from 'backbone.marionette';

import feedTemplate from 'Templates/layouts/feed.html';
import emptyTemplate from 'Templates/components/Thread/empty.html';

import { Threads, Categories } from '../collections';
import EditCategoryModal from '../components/Feed/EditCategoryModal';
import CategoryNavbar from '../components/Feed/CategoryNavbar';
import ThreadCollectionView from '../components/Feed/ThreadCollectionView';
import ThreadList from '../components/Feed/ThreadList';
import NewThreadModal from '../components/Feed/NewThreadModal';
import ThreadLink from '../components/Thread/Link';

import 'Styles/feed.less';

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
    newThreadButton: '.js-new-thread',
  },

  events: {
    'click @ui.newThreadButton': 'showNewThreadModal',
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

    this.listenTo(this.categories, 'change reset', this.fillNavCategories);
    this.listenTo(this.threads, 'reset', this.scrollToTop);
  },

  onRender() {
    // Navbar for filtering by category
    this.showChildView('categoryNavbar', new CategoryNavbar({ categories: this.navCategories }));
    // Modal for choosing preferred categories
    this.showChildView('categoryModal', new EditCategoryModal({ categories: this.categories }));
    this.categories.fetch({
      reset: true,
      success: () => {
        this.showChildView('newThreadModal', new NewThreadModal({ categories: this.categories }));
        M.AutoInit();
      },
    });

    M.Modal.init(this.$('.new-thread-modal'));
    // Main Feed
    this.getUI('scrollElement').height($(window).height() - $('nav').height());
    this.threads.fetch({
      success: () => {
        this.showChildView(
          'feed',
          new ThreadList({
            threads: this.threads,
            emptyView: EmptyView,
          }),
        );
      },
    });

    // Draft Threads
    this.showChildView(
      'drafts',
      new ThreadList({
        threads: this.draftThreads,
        title: 'My Drafts',
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

  /**
   * Sets the navigation bar categories list and adds the 'All' option
   */
  fillNavCategories() {
    this.navCategories.reset(this.categories.models);
    this.navCategories.add({ name: 'All', id: -1, preferred: true });
  },

  /**
   * Filters the main feed threads by fetching based on the category chosen
   * @param {Marionette.View} childView
   */
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

  /**
   * Opens the Category choosing Modal
   */
  showCategoryModal() {
    this.getChildView('categoryModal').openModal();
  },

  /**
   * Opens the New Thread Creation Modal
   */
  showNewThreadModal() {
    this.getChildView('newThreadModal').openModal();
  },

  /**
   * Auto scroll to the top of the list
   */
  scrollToTop() {
    $(this.getUI('scrollElement')).scrollTop(0);
  },
});

export default FeedView;

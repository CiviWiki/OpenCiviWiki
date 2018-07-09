import { View, CollectionView } from "backbone.marionette";

import { Threads, Categories } from "../collections";
import EditCategoryModal from "../components/Feed/EditCategoryModal";
import CategoryNavbar from "../components/Feed/CategoryNavbar";
import ThreadCollectionView from "../components/Feed/ThreadCollectionView";
import ThreadList from "../components/Feed/ThreadList";

import ThreadLink from "../components/Thread/Link";

import feedTemplate from "templates/layouts/feed.html";
import emptyTemplate from "templates/components/Thread/empty.html";

import "styles/feed.less";

const EmptyView = View.extend({
  template: emptyTemplate
});

const FeedView = View.extend({
  tagName: "div",
  className: "FeedView",
  id: "feed",
  template: feedTemplate,

  regions: {
    categoryModal: ".categories-modal-holder",
    newThreadModal: ".new-thread-modal-holder",
    categoryNavbar: ".navbar-container",
    trending: "#trending-list",
    feed: "#feed-list",
    drafts: "#drafts-list"
  },

  ui: {
    scrollElement: ".scroll-col",
  },

  childViewEvents: {
    "click:categoryItem": "filterFeed",
    "click:categoryManageButton": "showCategoryModal"
  },

  initialize() {
    this.threads = new Threads();
    this.draftThreads = new Threads();
    this.topThreads = new Threads();
    this.categories = new Categories();
    this.navCategories = new Categories();

    this.filterCategoryId = { id: -1 };

    this.listenTo(this.categories, "reset", this.fillNavCategories);
  },

  onRender() {
    // Navbar for filtering by category
    this.showChildView(
      "categoryNavbar",
      new CategoryNavbar({ categories: this.navCategories })
    );
    // Modal for choosing preferred categories
    this.showChildView(
      "categoryModal",
      new EditCategoryModal({ categories: this.categories })
    );
    this.categories.fetch({ reset: true });

    // Main Feed
    this.showChildView(
      "feed",
      new ThreadList({
        threads: this.threads,
        emptyView: EmptyView
      })
    );
    this.getUI("scrollElement").height($(window).height() - $("nav").height());
    this.threads.fetchAll();

    // Draft Threads
    this.showChildView(
      "drafts",
      new ThreadList({
        threads: this.draftThreads,
        title: "drafts"
      })
    );
    this.draftThreads.fetchDrafts();

    // "Trending" threads
    this.showChildView(
      "trending",
      new ThreadCollectionView({
        collection: this.topThreads,
        childView: ThreadLink
      })
    );
    this.topThreads.fetchTop({
      success: data => {
        console.log(data);
      }
    });

    
  },

  fillNavCategories() {
    this.navCategories.reset(this.categories.models);
    this.navCategories.add({ name: "All", id: "-1", preferred: true });
  },
  // fillFilteredThreads() {
  //   console.log(this.filterCategoryId)
  //   this.filteredThreads = this.filteredThreads.reset(this.threads.filterByCategory(this.filterCategoryId));
  // },

  filterFeed(childView) {
    if (childView.activeCategory === -1) {
      this.threads.fetch({ reset: true });
    } else {
      this.threads.fetch({
        data: { category_id: childView.activeCategory },
        reset: true
      });
    }
    // console.log(childView.activeCategory , "filter feed", this.threads);

    // this.fillFilteredThreads();

    // this.getChildView('feed').resetThreads();

    // var target = $(event.target);
    // console.log(target);

    // this.filteredThreads = this.filteredThreads.reset(
    //   this.feedThreads.filterByCategory(this.filterCategoryId)
    // );

    // var selectedCategory = target.data("id");
    // if (selectedCategory === "arrow") {
    //   return;
    // } else {
    //   if (selectedCategory === "all") {
    //     this.threads = this.options.threads.toJSON();
    //   } else if (_.contains(this.options.user_categories, selectedCategory)) {
    //     this.threads = JSON.parse(
    //       JSON.stringify(this.options.threads.filterCategory(selectedCategory))
    //     );
    //   }
    //   this.renderFeedList();
    //   this.$(".category-item").removeClass("active");
    //   target.addClass("active");
    // }
  },

  showCategoryModal() {
    this.getChildView("categoryModal").openModal();
  },

  showIndex() {
    //   Bb.history.navigate(""); // Update the location bar
    // },
    // showNoteList() {
    //   this.showChildView(
    //     "main",
    //     new NoteListView({
    //       collection: this.collection
    //     })
    //   );
    //   Bb.history.navigate("notes"); // Update the location bar
    // }
    // showNote(noteId) {
    //   const model = new NoteModel({ id: noteId });
    //   this.showChildView('main', new NoteDetailView({
    //     model: model
    //   }));
    //   model.fetch();
    //   Bb.history.navigate(`notes/${noteid}`);  // Update the location bar
    // },
    // showEditNote(noteId) {
    //   const model = new NoteModel({ id: noteId });
    //   this.showChildView('main', new NoteEditView({
    //     model: model
    //   }));
    //   model.fetch();
    //   Bb.history.navigate(`notes/${noteId}/edit`);  // Update the location bar
  }
});

export default FeedView;

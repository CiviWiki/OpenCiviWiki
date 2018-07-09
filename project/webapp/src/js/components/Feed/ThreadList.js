import { View } from "backbone.marionette";

import ThreadCollectionView from "../Feed/ThreadCollectionView";
import threadlistTemplate from "templates/components/Feed/thread_list.html";
import EmptyView from "../EmptyView";

const ThreadList = View.extend({
  tagName: "div",
  className: "ThreadList",
  template: threadlistTemplate,

  regions: {
    list: "#thread-list"
  },

  templateContext: function() {
    // Render title if present
    const context = {};
    if (this.title == "drafts") {
      context.title = `Your Drafts ${this.threads.length}`
    } else {
      context.title = ""
    }
    return context;
  },

  initialize() {
    this.threads = this.getOption("threads");
    this.emptyView = this.getOption("emptyView");
    this.title = this.getOption("title", "");
  },

  onRender() {
    this.renderThreads();
  },

  renderThreads() {
    // Attatch appropriate empty view 
    const options = { collection: this.threads };
    if (this.emptyView) {
      options.emptyView = this.emptyView;
    } else {
      options.emptyView = EmptyView;
    }
    this.showChildView("list", new ThreadCollectionView(options));
  }
});

export default ThreadList;

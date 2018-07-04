import { View } from "backbone.marionette";
import { Account, Category, Thread } from "../models";
import feedTemplate from "../../templates/views/test.html";

const FeedView = View.extend({
  el: "#app-hook",
  template: _.template(feedTemplate()),

//   templateContext: {
//     categories: this.collection
//   },
  regions: {
    feedList: "#main-threads",
    trendingList: "#trending-threads"
  }
});

export default FeedView;

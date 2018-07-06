import { View, CollectionView } from "backbone.marionette";
import { Account, Category, Thread } from "../models";

import feedTemplate from "templates/views/test.html";
import feedSubTemplate from "templates/views/subtest.html";

import 'styles/feed.less';


const TestItemView = View.extend({
  template: feedSubTemplate,
});

const TestCollectionView = CollectionView.extend({
  tagName: 'ul',
  className: 'test-collection',
  childView: TestItemView,

  isEmpty: function(options) {
    // some logic to calculate if the view should be rendered as empty
    return this.collection.length == 0;
  }
  // initialize: () => {
  //   this.listenTo(this.collection, 'change', this.render);
  // },
  // regions: {
  //   regionTest: "#regionTest"
  // }
});

const FeedView = View.extend({
  el: "#app-hook",
  template: feedTemplate,
  // childView: TestCollectionView,

  onRender() {
    this.showChildView('regionTest', new TestCollectionView({collection: this.collection}));
  },
  regions: {
    regionTest: "#regionTest"
  }
});


export default FeedView;

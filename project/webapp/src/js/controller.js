import { Object } from "backbone.marionette";

import RootView from "./views/RootView";
import FeedView from "./views/FeedView";

const AppController = Object.extend({
  initialize() {
    this.rootView = new RootView({context: this.getOption("context")});
    this.app = this.getOption("app");
    this.app.showView(this.rootView);
  },

  viewMainFeed() {
    const feedView = new FeedView();
    this.rootView.renderContent(feedView);
  },

  showThread() {},

  showTest() {
    const allCategories = new Categories();
    const main = new TestView({ collection: allCategories });
    main.render();
    allCategories.fetch();
  }
});

export default AppController;

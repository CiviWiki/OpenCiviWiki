import { Object } from "backbone.marionette";
import { Categories, Threads, Notifications } from "./collections";
import { Account } from "./models";

import RootView from "./views/RootView";
import FeedView from "./views/FeedView";

const AppController = Object.extend({
  initialize() {
    this.currentUser = new Account({
      username: this.getOption("context").username
    });
    this.notifications = new Notifications();

    this.rootView = new RootView({
      account: this.currentUser,
      notifications: this.notifications
    });
    this.currentUser.fetch();
    this.notifications.startFetchPoll();

    const app = this.getOption("app");
    app.showView(this.rootView);
  },

  viewMainFeed() {
    const feedData = {
      categories: new Categories(),
      feedThreads: new Threads(),
      draftThreads: new Threads(),
      topThreads: new Threads()
    };

    const feed = new FeedView(feedData);
    this.rootView.renderContent(feed);
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

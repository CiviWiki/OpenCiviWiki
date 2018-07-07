import { Object } from "backbone.marionette";
import Categories from "./collections/Categories";
import { Account } from "./models";

import RootLayout from "./views/RootLayout";

const AppController = Object.extend({
  initialize() {
    this.currentUser = new Account({ username: this.getOption("context").username });

    this.rootView = new RootLayout({ account: this.currentUser });
    this.currentUser.fetch();

    const app = this.getOption("app");
    app.showView(this.rootView);
  },

  viewMainFeed() {},

  showThread() {},

  showTest() {
    const allCategories = new Categories();
    const main = new TestView({ collection: allCategories });
    main.render();
    allCategories.fetch();
  }
});

export default AppController;

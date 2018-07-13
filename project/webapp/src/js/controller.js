import { Object } from 'backbone.marionette';
import { history } from 'backbone';
import { Account } from './models';
import RootView from './views/RootView';
import FeedView from './views/FeedView';
import ErrorView from './views/ErrorView';
import ProfileView from './views/ProfileView';

const AppController = Object.extend({
  initialize() {
    this.context = this.getOption('context');
    this.rootView = new RootView({ context: this.context });
    this.app = this.getOption('app');
    this.app.showView(this.rootView);
  },

  viewMainFeed() {
    const feedView = new FeedView();
    this.rootView.renderContent(feedView);
  },

  viewThread() {},

  viewProfile(username) {
    this.account = new Account({ username });

    const profileView = new ProfileView({
      model: this.account,
      context: this.context,
    });
    this.account.fetchProfile();

    this.rootView.renderContent(profileView);
  },

  showErrorPage() {
    const errorView = new ErrorView();
    this.rootView.renderContent(errorView);
  },
});

export default AppController;

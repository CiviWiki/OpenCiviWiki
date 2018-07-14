import { Object } from 'backbone.marionette';
import { Account, Thread } from './models';
import RootView from './views/RootView';
import FeedView from './views/FeedView';
import ErrorView from './views/ErrorView';
import ProfileView from './views/ProfileView';
import UserSetupView from './views/UserSetupView';
import ThreadView from './views/ThreadView';

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

  viewThread(threadId) {
    const appContext = this.context;
    const thread = new Thread({ id: threadId });

    const threadView = new ThreadView({
      model: thread,
      context: appContext,
    });
    thread.fetch();
    this.rootView.renderContent(threadView);
  },

  viewProfile(username) {
    const account = new Account({ username });

    const profileView = new ProfileView({
      model: account,
      context: this.context,
    });
    account.fetchProfile();

    this.rootView.renderContent(profileView);
  },

  viewSetup() {
    this.account = new Account({ username: this.context.username });
    const setupView = new UserSetupView({
      model: this.account,
      context: this.context,
    });
    this.account.fetch();
    this.rootView.renderContent(setupView);
  },

  showErrorPage() {
    const errorView = new ErrorView();
    this.rootView.renderContent(errorView);
  },
});

export default AppController;

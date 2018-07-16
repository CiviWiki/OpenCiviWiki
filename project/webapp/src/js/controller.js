import { Object } from 'backbone.marionette';
import { Account, Thread } from './models';

import ErrorView from './views/ErrorView';
import FeedView from './views/FeedView';
import InviteView from './views/InviteView';
import LoginView from './views/LoginView';
import ProfileView from './views/ProfileView';
import RootView from './views/RootView';
import SettingsView from './views/SettingsView';
import ThreadView from './views/ThreadView';
import UserSetupView from './views/UserSetupView';

const AppController = Object.extend({
  initialize() {
    this.context = this.getOption('context');
    this.app = this.getOption('app');
    if (this.context.username) {
      this.rootView = new RootView({ context: this.context });
      this.app.showView(this.rootView);
    }
  },

  viewLogin() {
    const loginView = new LoginView();
    this.app.showView(loginView);
  },

  viewMainFeed() {
    const feedView = new FeedView();
    this.rootView.renderContent(feedView);
  },

  viewInvite() {
    this.context.data = JSON.parse(this.context.data);

    const inviteView = new InviteView({ context: this.context });
    this.rootView.renderContent(inviteView);
    inviteView.renderInvitees();
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

  viewSettings() {
    this.account = new Account({ username: this.context.username });
    const settingsView = new SettingsView({
      model: this.account,
      context: this.context,
    });
    this.account.fetch();
    this.rootView.renderContent(settingsView);
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

  showErrorPage() {
    const errorView = new ErrorView();
    this.rootView.renderContent(errorView);
  },
});

export default AppController;

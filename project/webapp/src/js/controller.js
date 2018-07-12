import { Object } from 'backbone.marionette';
import { history } from 'backbone';
import RootView from './views/RootView';
import FeedView from './views/FeedView';
import ErrorView from './views/Error';
// import { Account } from './models';
// import ProfileView from './views/ProfileView';

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

  viewMyProfile() {
    // console.log('view my profile');
    // history.navigate(`profile/${this.context.username}`, { trigger: true });
  },

  viewProfile() {
    // this.account = new Account({ username });
    // const profileView = new ProfileView({
    //   model: this.account,
    //   options: this.getOption('context'),
    // });
    // this.account.fetch();
    // this.rootView.renderContent(profileView);
    console.log('view profile');
  },

  showErrorPage() {
    const errorView = new ErrorView();
    this.rootView.renderContent(errorView);
  },
});

export default AppController;

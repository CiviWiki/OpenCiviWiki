import { AppRouter } from 'backbone.marionette';
import { FeedController, ProfileController, ThreadController } from './controllers'
const Controller = Mn.Object.extend({
  initialize() {
    // this.layout = new AppLayout();
    const app = this.getOption('app');
    app.showView(layout);
  },

  static() {
    this.layout.showStaticPages();
  },

  threads() {
    this.layout.showThreads();
  },

  viewThread(noteId) {
    this.layout.showNote(parseInt(noteId));
  },
});

var OverviewRouter = AppRouter.extend({
  appRoutes: {
    'overview': 'overviewcontent'
 },

 controller: new OverviewController({region: options.region});
});

const controllers = {
  'showFeed': FeedController,
  'showThread': ThreadController,
  'showProfile': ProfileController,
}
const Router = AppRouter.extend({
  controller : controllers,

  appRoutes: {
    '/login': 'login', 
    '/invite': 'invite',
    '/setup': 'setup',
    '/settings' : 'settings',

    '/' : 'showFeed',
    '/threads': 'showThreadList',
    '/thread/:threadId': 'showThread',
    '/thread/:threadId/edit': 'editThread',

    '/profile/:username': 'showProfile',
  }
});

export default Router;
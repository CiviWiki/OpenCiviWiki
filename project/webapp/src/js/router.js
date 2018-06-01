import { AppLayout } from './views/layout';

const Controller = Mn.Object.extend({
  initialize() {
    this.layout = new AppLayout();
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

export const Router = Mn.AppRouter.extend({
  initialize() {
    this.controller = new Controller(this.options);
  },

  appRoutes: {
    // Static Pages
    '/': 'index',
    '/about': 'about',
    '/support_us': 'support_us',
    '/howitwors': 'howItWorks',

    '/login': 'login', 
    '/invite': 'invite',
    '/setup': 'setup',
    '/settings' : 'settings',

    '/threads': 'showThreadList',
    '/thread/:threadId': 'showThread',
    '/thread/:threadId/edit': 'editThread',
    '/profile/:username': 'showProfile',
  }
});

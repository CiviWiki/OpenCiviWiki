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
    'app/': 'index',
    'app/threads': 'showThreadList',
    'app/thread/:threadId': 'showThread',
    'threads/:threadId/edit': 'editThread'
    'app/profile/:username': 'showProfile',

  }
});

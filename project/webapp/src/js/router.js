import { AppRouter } from 'backbone.marionette';
import AppController from './controller';

const Router = AppRouter.extend({
  initialize(options) {
    this.controller = new AppController(options);
  },

  appRoutes: {
    '': 'viewMainFeed',
    'setup(/)': 'viewSetup',
    'thread/:threadId': 'viewThread',
    'profile/(:username)': 'viewProfile',
    '*invalidRoute': 'showErrorPage',
  },
});

export default Router;

// '/invite': 'invite',
// '/settings' : 'settings',

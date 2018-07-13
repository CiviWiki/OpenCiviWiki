import { AppRouter } from 'backbone.marionette';
import AppController from './controller';

const Router = AppRouter.extend({
  initialize(options) {
    this.controller = new AppController(options);
  },

  appRoutes: {
    // '/login': 'login',
    // '/invite': 'invite',
    // '/setup': 'setup',
    // '/settings' : 'settings',

    '': 'viewMainFeed',
    'thread/:threadId': 'viewThread',
    'profile/(:username)': 'viewProfile',
    '*invalidRoute': 'showErrorPage',
  },
});

export default Router;

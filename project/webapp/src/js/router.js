import { AppRouter } from 'backbone.marionette';
import AppController from './controller';

const Router = AppRouter.extend({
  initialize(options) {
    this.controller = new AppController(options);
  },

  appRoutes: {
    '': 'viewMainFeed',
    // '/login': 'login',
    // '/invite': 'invite',
    'setup': 'viewSetup',
    // '/settings' : 'settings',

    
    'thread/:threadId': 'viewThread',
    'profile/(:username)': 'viewProfile',
    '*invalidRoute': 'showErrorPage',
  },
});

export default Router;

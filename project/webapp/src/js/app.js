import 'materialize-css';
import { Application } from 'backbone.marionette';
import { history } from 'backbone';

import Router from './router';
import CSRFToken from './utils/csrftoken';

const App = Application.extend({
  region: 'main',
  initialize() {
    this.context = this.getOption('context');
  },

  onStart() {
    this.router = new Router({
      app: this,
      context: this.context,
    });

    CSRFToken();
    history.start({ root: '/', pushState: true });
  },
});

window.startApp = (context) => {
  const app = new App({ context });
  app.start();
};

import Application from 'backbone.marionette';
import history from 'backbone';

import Router from './router';


const MyApp = Application.extend({
  onStart() {
    this.router = new Router({ app: this });
  
    history.start({ root: '/app', pushState: true });
  }
});

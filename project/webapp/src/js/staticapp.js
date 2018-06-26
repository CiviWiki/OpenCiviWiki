import Application from 'backbone.marionette'

import Router from "./approuter";
import CSRFToken from "./utils/csrftoken";
import { StaticController } from './controllers/static'

const App = Application.extend({
  onStart() {
    this.router = new Router({ app: this });
    CSRFToken();
  }
});

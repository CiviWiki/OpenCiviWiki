import { Application } from "backbone.marionette";
import { history } from "backbone";

import "materialize-css";
import "materialize-css/dist/css/materialize.css";
import "styles/utils.less";

import Router from "./router";
import CSRFToken from "./utils/csrftoken";


const App = Application.extend({
  region: "main",
  initialize() {
    this.context = this.getOption("context");
  },

  onStart() {
    this.router = new Router({
      app: this,
      context: this.context
    });

    CSRFToken();
    history.start({ root: "/", pushState: true });
  }
});

window.startApp = context => {
  const app = new App({ context: context });
  app.start();
};

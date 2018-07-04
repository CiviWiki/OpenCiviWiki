import { Application } from "backbone.marionette";
import Router from "./approuter";
import CSRFToken from "./utils/csrftoken";

const App = Application.extend({
  onStart() {
    this.router = new Router({ app: this });
    CSRFToken();
    Bb.history.start({ root: "/", pushState: true });
  }
});

var app = new App();
app.start();

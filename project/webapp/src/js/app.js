import Router from "./router";
import CSRFToken from "./utils/csrftoken";

const App = Mn.Application.extend({
  onStart() {
    this.router = new Router({ app: this });

    Bb.history.start({ root: "/", pushState: true });
  }
});

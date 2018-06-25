import { Object } from "backbone.marionette";
import AboutView from "./static/about_view.js";
import HowItWorksView from "./static/how_it_works_view.js";
import LandingView from "./static/landing_view.js";
import SupportUsView from "./static/suppot_us_view.js";

const StaticController = Object.extend({
  viewLanding() {
    LandingView();
  },
  viewAbout() {
    AboutView();
  },
  viewHowItWorks() {
    HowItWorksView();
  },
  viewSupportUs() {
    SupportUsView();
  },
  viewLogin() {
    this.layout.showThreads();
  }
});

export default StaticController;

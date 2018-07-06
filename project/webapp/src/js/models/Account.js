import { Model } from "backbone";

const Account = Model.extend({
  defaults: function() {
    return {
      profile_image: "",
      username: "",
      first_name: "",
      last_name: "",
      about_me: "",
      location: "",
      history: [],
      followers: [],
      following: [],
      issues: [],
      representatives: []
    };
  },
  urlRoot: "/api/v1/accounts/",

  idAttribute: "username",

  fetchCurrent: () => {
    url = `${this.urlRoot}`;
    this.fetch(url);
    return this;
  },

  initialize: (model, options) => {
    options = options || {};
    this.user = options.user;
  }
});

export default Account;

import { Model } from "backbone";

const Category = Model.extend({
  defaults: function() {
    return {
      username: "",
      first_name: "",
      last_name: "",
      about_me: ""
    };
  },
  urlRoot: "/api/v1/accounts/",

  idAttribute: "username",
  initialize: function(model, options) {
    options = options || {};
  }
});

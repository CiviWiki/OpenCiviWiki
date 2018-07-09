import { Model } from "backbone";

const Thread = Model.extend({
  defaults: function() {
    return {
      id: 0,
      title: "",
      summary: "",
      author: "",
      image: "",
      created: "",
      created_str: "",
      is_draft: true
    };
  },
  urlRoot: "/api/v1/threads/",

  idAttribute: "id",

  parse: data => {
    data.created = new Date(data.created);
    data.created_str = data.created.toLocaleString("en-us", {
      year: "numeric",
      month: "long",
      day: "numeric"
    });
    return data;
  },

  initialize: (model, options) => {
    options = options || {};
  }
});

export default Thread;

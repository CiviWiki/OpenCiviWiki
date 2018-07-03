import { Model } from "backbone";

const Thread = Model.extend({
  defaults: function() {
    return {
      id: "",
      title: "",
      summary: "",
      author: "",
      image: "",
      created: "",
      is_draft: ""
    };
  },
  urlRoot: "/api/v1/threads/",

  idAttribute: "id",
  
  initialize: (model, options) => {
    options = options || {};
  }
});

export default Thread;
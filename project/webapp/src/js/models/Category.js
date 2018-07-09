import { Model } from "backbone";

const Category = Model.extend({
  defaults: function() {
    return {
      id: "",
      name: "",
      preferred: true,
    };
  },
  urlRoot: "/api/v1/categories/",

  idAttribute: "id",

  initialize: (model, options) => {
    options = options || {};
  }
});

export default Category;

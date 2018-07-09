import { Collection } from "backbone";
import { Category } from "../models";

const Categories = Collection.extend({
  model: Category,
  url: "/api/v1/categories",
  comparator: "id",

  fetchByUsername(username) {
    this.url = `/api/v1/account/${username}/categories`;
    this.fetch();
    return this;
  },

  filterById /* prev:filterCategory */: category_id => {
    const filtered = this.models.filter(model => {
      return model.get("category") === category_id;
    });
    return filtered;
  }
});

export default Categories;

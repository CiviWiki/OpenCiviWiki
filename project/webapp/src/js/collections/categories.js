import { Collection } from "backbone";
import { Category } from "../models";

const Categories = Collection.extend({
  model: Category,
  url: "/api/v1/categories",
  comparator: "id",

  filterById /* prev:filterCategory */: category_id => {
    var filtered = this.models.filter(model => {
      return model.get("category") === category_id;
    });
    return filtered;
  }
});

export default Categories;

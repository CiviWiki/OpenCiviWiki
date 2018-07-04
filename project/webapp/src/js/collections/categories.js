import { Collection } from "backbone";
import { Category } from "../models";

const Categories = Collection.extend({
  model: Category,
  url: "/api/v1/categories",
  comparator: "id",
  fetchTrending: () => {},
  fetchDrafts: () => {},

  filterCategory: function(category_id) {
    var filtered = this.models.filter(function(thread_data) {
      return thread_data.get("category") === category_id;
    });
    return filtered;
  }
});

export default Categories;

import { Collection } from "backbone";
import { Thread } from "../models";

const Threads = Collection.extend({
  model: Thread,
  url: "/api/v1/threads",

  comparator: model => {
    return -model.get("created").getTime();
  },

  fetchAll() {
    this.url = `${this.url}/all`;
    this.fetch();
  },
  fetchTop() {
    this.url = `${this.url}/top`;
    this.fetch();
  },
  fetchDrafts() {
    this.url = `${this.url}/drafts`;
    this.fetch();
  },

  filterByCategory(categoryId) {
    if (categoryId === -1) {
      return this.models;
    }
    const filtered = this.models.filter(function(model) {
      return model.get("category").id === categoryId;
    });
    return filtered;
  }
});

export default Threads;

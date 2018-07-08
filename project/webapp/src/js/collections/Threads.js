import { Collection } from "backbone";
import { Thread } from "../models";

const Threads = Collection.extend({
  model: Thread,
  url: "/api/v1/threads",

  comparator: model => {
    return -model.get("date").getTime();
  },

  fetchAll: () => {
    url = `${this.url}/all`;
    this.fetch(url);
    return this;
  },
  fetchTop: () => {
    url = `${this.url}/top`;
    this.fetch(url);
    return this;
  },
  fetchDrafts: () => {
    url = `${this.url}/drafts`;
    this.fetch(url);
    return this;
  },

  filterCategory: function(category_id) {
    var filtered = this.models.filter(function(thread_data) {
      return thread_data.get("category") === category_id;
    });
    return filtered;
  }
});

export default Threads;

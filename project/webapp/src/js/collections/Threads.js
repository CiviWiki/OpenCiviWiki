import { Collection } from 'backbone';
import { Thread } from '../models';

const Threads = Collection.extend({
  model: Thread,
  url: '/api/v1/threads',

  comparator: (model) => {
    if (model.get('created')) {
      return -model.get('created').getTime();
    }
    return model.id;
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
    const filtered = this.models.filter(model => model.get('category').id === categoryId);
    return filtered;
  },
});

export default Threads;

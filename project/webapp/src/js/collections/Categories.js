import { Collection } from 'backbone';
import { Category } from '../models';

const Categories = Collection.extend({
  model: Category,
  url: '/api/v1/categories',
  comparator: 'id',

  fetchByUsername(username) {
    this.url = `/api/v1/account/${username}/categories`;
    this.fetch();
    return this;
  },

  filterById: (categoryId) => {
    const filtered = this.models.filter(model => model.get('category') === categoryId);
    return filtered;
  },
});

export default Categories;

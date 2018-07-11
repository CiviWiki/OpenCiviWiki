import { Model } from 'backbone';

const Category = Model.extend({
  defaults() {
    return {
      id: '',
      name: '',
      preferred: true,
    };
  },
  urlRoot: '/api/v1/categories/',

  idAttribute: 'id',
});

export default Category;

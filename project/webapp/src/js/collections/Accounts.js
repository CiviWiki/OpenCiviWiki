import { Collection } from 'backbone';
import { Account } from '../models';

const Categories = Collection.extend({
  model: Account,
  url: '/api/v1/accounts',
  comparator: 'username',
});

export default Categories;

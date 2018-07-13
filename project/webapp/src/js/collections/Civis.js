import { Collection } from 'backbone';
import { Civi } from '../models';

const Civis = Collection.extend({
  model: Civi,
  url: '/api/v1/civis',
  comparator: 'id',
});

export default Civis;

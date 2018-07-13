import { Collection } from 'backbone';
import { Civi } from '../models';

const Civis = Collection.extend({
  model: Civi,
  url() {
    return `/api/response_data/${this.threadId}/${this.civiId}/`;
  },
  comparator: 'id',

  initialize(model, options) {
    this.threadId = options.threadId;
    this.civiId = null;
  },
  filterByType(type) {
    const filtered = this.models.filter(civi => civi.get('type') === type);
    return filtered;
  },
});

export default Civis;

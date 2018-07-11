import { Model } from 'backbone';

const Notification = Model.extend({
  defaults: {
    actor: 'username',
    verb: 'performed an action',
    target: 'object',
    timestamp: Date.now(),
    data: {},
  },

  parse(response) {
    response.data = JSON.parse(response.data);
    return response;
  },
});

export default Notification;

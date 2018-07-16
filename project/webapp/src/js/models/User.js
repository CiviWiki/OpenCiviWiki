import { Model } from 'backbone';

const User = Model.extend({
  defaults() {
    return {
      username: '',
      email: '',
      location: '',
    };
  },
  urlRoot: '/api/account_profile/',
  idAttribute: 'username',
});

export default User;

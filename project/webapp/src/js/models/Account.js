import { Model } from 'backbone';

const Account = Model.extend({
  defaults: {
    profile_image_url: '',
    profile_image_thumb_url: '',
    username: '',
    first_name: '',
    last_name: '',
    about_me: '',
    location: '',
    civis: [],
    followers: [],
    following: [],
    issues: [],
    representatives: [],
    is_staff: false,
  },
  urlRoot: '/api/v1/accounts/',

  idAttribute: 'username',

  fetchCurrent() {
    const url = `${this.urlRoot}`;
    this.fetch(url);
    return this;
  },
});

export default Account;

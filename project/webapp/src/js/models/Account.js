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
  url() {
    return `${this.urlRoot}${this.id}/`;
  },
  idAttribute: 'username',

  fetchCurrent() {
    this.url = `${this.urlRoot}`;
    this.fetch();
    this.url = `${this.urlRoot}${this.id}/`;
  },

  fetchProfile() {
    this.url = `/api/account_profile/${this.id}/`;
    this.fetch();
  },

  fetchCard() {
    this.url = `/api/account_profile/${this.id}/`;
    this.fetch();
    this.url = `${this.urlRoot}${this.id}/`;
  },
});

export default Account;

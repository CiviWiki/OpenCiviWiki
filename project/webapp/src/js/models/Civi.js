import { Model } from 'backbone';

const Civi = Model.extend({
  defaults() {
    return {
      id: 0,
      title: '',
      summary: '',
      author: '',
      image: '',
      created: '',
      created_str: '',
      is_draft: true,
    };
  },
  urlRoot: '/api/v1/civis/',

  idAttribute: 'id',

  parse: (data) => {
    const modelData = data;
    modelData.created = new Date(data.created);
    modelData.created_str = data.created.toLocaleString('en-us', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
    return modelData;
  },
});

export default Civi;

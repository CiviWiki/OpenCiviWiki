import { View } from 'backbone.marionette';

const LinkSelectView = View.extend({
  el: '#magicsuggest',

  initialize(options) {
    this.options = options || {};
    this.civis = options.civis;

    this.$el = options.$el || this.$el;
    this.setElement(this.$el);
    this.render();

    return this;
  },

  render() {
    const _this = this;

    this.ms = this.$el.magicSuggest({
      allowFreeEntries: false,
      groupBy: 'type',
      valueField: 'id',
      displayField: 'title',
      expandOnFocus: true,
      data: [],
      renderer(data) {
        return (
          `<div class="link-lato" data-civi-id="${
            data.id
          }"><span class="gray-text">${
            data.type
          }</span> ${
            data.title
          }</div>`
        );
      },
      selectionRenderer(data) {
        return (
          `<span class="gray-text bold-text">${data.type.toUpperCase()}</span> ${data.title}`
        );
      },
    });
  },

  setLinkableData(c_type) {
    const _this = this;
    let linkableCivis = [];
    if (c_type == 'cause') {
      linkableCivis = _this.civis.where({ type: 'problem' });
    } else if (c_type == 'solution') {
      linkableCivis = _this.civis.where({ type: 'cause' });
    }
    const msdata = [];
    _.each(linkableCivis, (c_model) => {
      const civi = {
        id: c_model.get('id'),
        type: c_model.get('type'),
        title: c_model.get('title'),
      };
      msdata.push(civi);
    });
    // console.log(msdata);
    this.ms.setData(msdata);

    return this;
  },
});
export default LinkSelectView;

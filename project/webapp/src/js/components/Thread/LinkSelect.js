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

  setLinkableData(civiType) {
    const view = this;
    let linkableCivis = [];
    if (civiType === 'cause') {
      linkableCivis = view.civis.where({ type: 'problem' });
    } else if (civiType === 'solution') {
      linkableCivis = view.civis.where({ type: 'cause' });
    }
    const msdata = [];
    _.each(linkableCivis, (civiModel) => {
      const civi = {
        id: civiModel.get('id'),
        type: civiModel.get('type'),
        title: civiModel.get('title'),
      };
      msdata.push(civi);
    });
    // console.log(msdata);
    this.ms.setData(msdata);

    return this;
  },
});
export default LinkSelectView;

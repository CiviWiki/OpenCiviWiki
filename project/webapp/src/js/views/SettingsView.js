import { View } from 'backbone.marionette';

const SettingsView = View.extend({
  el: '#settings',

  initialize(options) {
    this.options = options || {};
    this.mapView = options.mapView;

    this.template = _.template($('#settings-template').text());
    this.settingsTemplate = _.template($('#settings-base').text());
    this.personalTemplate = _.template($('#settings-personal').text());
    this.locationLabelTemplate = _.template($('#location-label').text());

    this.listenTo(this.model, 'change', this.renderAllLabels);
  },

  render() {
    this.$el.html(this.template());

    this.$('#settings-el').html(this.settingsTemplate());

    this.renderPersonal();

    this.mapView.renderAndInitMap();
    this.listenTo(this.mapView.model, 'change:is_new', _.bind(this.saveLocation, this));
  },

  renderAllLabels() {
    this.renderPersonal();
    this.renderLocationLabel();
    M.updateTextFields();
  },

  renderPersonal() {
    this.$('#settings-1').html(this.personalTemplate());
  },

  renderLocationLabel() {
    this.$('#location-label-container').html(this.locationLabelTemplate());
  },

  events: {
    'blur .save-account': 'saveAccount',
  },

  saveAccount(e) {
    const $this = $(e.target);
    const changeKey = $this.attr('id');
    const changeVal = $this.val().trim();
    const apiData = {};
    const view = this;

    if (this.model.get([changeKey]) === changeVal) {
      return;
    }
    apiData[changeKey] = changeVal;

    $.ajax({
      url: '/api/edituser/',
      type: 'POST',
      data: apiData,
      success() {
        M.toast({ html: 'Saved!' });
        view.isSave = true;
        view.model.fetch();
      },
    });
  },

  saveLocation() {
    const view = this;
    const coordinates = this.mapView.model.get('coordinates');


    const address = this.mapView.model.get('address');

    if (!this.mapView.model.get('is_new')) return;

    if (coordinates && address) {
      $.ajax({
        type: 'POST',
        url: '/api/edituser/',
        data: {
          coordinates,
          address: address.address,
          city: address.city,
          state: address.state,
          zip_code: address.zipcode,
          country: address.country,
          longitude: coordinates.lng,
          latitude: coordinates.lat,
        },
        success() {
          M.toast({ html: '<span class="subtitle-lato white-text">Location Changed</span>' });
          view.mapView.model.set('is_new', false);
          view.model.fetch();
        },
        error(response) {
          if (response.status_code === 400) {
            M.toast({ html: response.message });
          } else if (response.status_code === 500) {
            M.toast({ html: 'Internal Server Error' });
          } else {
            M.toast({ html: response.statusText });
          }
        },
      });
    }
  },
});

export default SettingsView;

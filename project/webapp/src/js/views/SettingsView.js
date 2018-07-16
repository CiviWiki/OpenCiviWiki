import { View } from 'backbone.marionette';

import baseTemplate from 'Templates/layouts/settings.html';
import { GoogleMap } from '../models';
import MapView from '../components/Map/MapView';
import Personal from '../components/Settings/Personal';

import 'Styles/map.less';
import 'Styles/utils.less';

const SettingsView = View.extend({
  template: baseTemplate,

  regions: {
    personal: '#personal-settings',
  },

  initialize() {
    this.listenTo(this.model, 'change', this.renderView);
  },

  renderView() {
    const locationData = {
      lng: this.model.get('longitude'),
      lat: this.model.get('latitude'),
    };
    this.googleAPIKey = this.getOption('context').GoogleAPIKey;
    this.mapView = new MapView({
      model: new GoogleMap({ coordinates: locationData }),
      googleMapsApiKey: this.googleAPIKey,
    });

    this.renderAllLabels();
    this.mapView.renderAndInitMap();
    this.listenTo(this.mapView.model, 'change:is_new', _.bind(this.saveLocation, this));
  },

  renderAllLabels() {
    this.showChildView('personal', new Personal({ model: this.model }));
    M.updateTextFields();
  },

  events: {
    'blur .save-account': 'saveAccount',
    'keypress .save-account': 'checkForEnter',
  },

  checkForEnter: (event) => {
    if (event.which === 13 && !event.shiftKey) {
      event.preventDefault();
      $(event.target).blur();
    }
  },

  saveAccount(event) {
    const $this = $(event.target);
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

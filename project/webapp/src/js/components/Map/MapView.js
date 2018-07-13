import { View } from 'backbone.marionette';
import baseTemplate from 'Templates/components/Map/map.html';

const MapView = View.extend({
  id: 'location',
  el: '#location',
  template: baseTemplate,

  events: {
    'click #browser-locate-btn': 'geolocate',
  },

  initialize() {
    this.googleMapsApiKey = this.getOption('googleMapsApiKey');
    return this;
  },

  renderAndInitMap(elId) {
    const view = this;
    view.id = elId || view.id;
    view.setElement($(`#${view.id}`));

    if (!this.loadedAPI) {
      this.loadedAPI = true;
      const url = `https://maps.googleapis.com/maps/api/js?key=${
        view.googleMapsApiKey
      }&libraries=places`;
      $.ajax({
        url,
        dataType: 'script',
        success() {
          view.render();
        },
      });
    }
  },

  render() {
    const viewElement = $(`#${this.id}`);
    this.setElement(viewElement);
    this.$el.empty().append(this.template);
    if (typeof google !== 'undefined') {
      this.model.initMapWithMarker(document.getElementById('map'));
      this.initAutocomplete();
      this.adjustMapCenter(this.model.get('coordinates'));
    }
  },

  // resizes the map to resolve grey-box sizing issues
  resizeMap() {
    google.maps.event.trigger(this.model.get('map'), 'resize');
    return this;
  },

  // moves the map and the marker per given coordinates
  adjustMapCenter(coordinates) {
    const mapCoordinates = coordinates || this.model.get('coordinates');
    this.model.set('coordinates', mapCoordinates);
    this.model.get('map').setCenter(mapCoordinates);
    this.model.get('marker').setPosition(mapCoordinates);
    return this;
  },

  // Create the autocomplete input object
  initAutocomplete() {
    const autocomplete = new google.maps.places.Autocomplete(
      document.getElementById('autocomplete'),
      {
        types: ['geocode'],
        componentRestrictions: {
          country: 'us',
        },
      },
    );
    autocomplete.addListener('place_changed', this.fillInAddress.bind(this));
    this.model.set('autocomplete', autocomplete);
  },

  // fillInAddress(): Get the address from the autocomplete object.
  fillInAddress() {
    this.$('.progress').toggleClass('hide');
    const place = this.model.get('autocomplete').getPlace();
    // Check if user didn't select any Options
    if (_.isUndefined(place.address_components)) {
      this.$('.progress').toggleClass('hide');
      return;
    }

    this.model.set('address', this.getAddressFromComponents(place.address_components));
    // Set the model's coordinates
    const coordinates = {
      lat: place.geometry.location.lat(),
      lng: place.geometry.location.lng(),
    };
    this.model.set('coordinates', coordinates);
    this.model.set('is_new', true);

    this.adjustMapCenter(coordinates);
    this.$('.progress').toggleClass('hide');
  },

  // geolocate(): Use the browser's location to get coordinate values
  geolocate() {
    const view = this;
    this.$('#browser-locate-btn')
      .addClass('disabled')
      .attr('disabled', true);
    this.$('#autocomplete')
      .addClass('disabled')
      .attr('disabled', true);
    this.$('.progress').removeClass('hide');
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const geolocation = {
            lat: Math.round(position.coords.latitude * 100000) / 100000,
            lng: Math.round(position.coords.longitude * 100000) / 100000,
          };
          if (_.isEqual(view.model.get('coordinates'), geolocation)) {
            this.$('.progress').addClass('hide');
            this.$('#browser-locate-btn')
              .removeClass('disabled')
              .attr('disabled', false);
            this.$('#autocomplete')
              .removeClass('disabled')
              .attr('disabled', false);
            return;
          }

          view.model.set('coordinates', geolocation);

          view.model.get('geocoder').geocode({ location: geolocation }, (results, status) => {
            if (status === 'OK') {
              view.$('#autocomplete').val(results[0].formatted_address);
              const fullAddress = view.getAddressFromComponents(results[0].address_components);
              if (fullAddress.country !== 'United States') {
                fullAddress.state = '';
                fullAddress.zipcode = '';
                M.toast({
                  html:
                    '<span>Please note that CiviWiki is optimized for the use in the U.S.</span>',
                });
              }
              view.adjustMapCenter(geolocation);
              view.model.set('address', fullAddress);
              view.model.set('is_new', true);
            } else {
              M.toast({
                html: `Geocode Error: ${status}`,
              });
            }
            this.$('.progress').addClass('hide');
            this.$('#browser-locate-btn')
              .removeClass('disabled')
              .attr('disabled', false);
            this.$('#autocomplete')
              .removeClass('disabled')
              .attr('disabled', false);
          });
        },
        () => {
          M.toast({
            html:
              "<span>We could not use your browser's location. Please try entering your location</span>",
          });
          this.$('.progress').addClass('hide');
          this.$('#autocomplete')
            .removeClass('disabled')
            .attr('disabled', false);
        },
      );
    } else {
      M.toast({
        html:
          "<span>We could not use your browser's location. Please try entering your location</span>",
      });
      this.$('.progress').addClass('hide');
      this.$('#autocomplete')
        .removeClass('disabled')
        .attr('disabled', false);
    }
  },

  getAddressFromComponents(addressComponents) {
    // Component variables we are interested in
    const components = {
      street_number: '', // Number
      route: '', // Street
      locality: '', // City
      administrative_area_level_1: '', // State
      postal_code: '', // Zipcode
      country: '', // Country
    };

    const options = {
      street_number: 'long_name', // Number
      route: 'long_name', // Street
      locality: 'long_name', // City
      administrative_area_level_1: 'short_name', // State
      postal_code: 'long_name', // Zipcode
      country: 'long_name', // Country
    };
    $.each(addressComponents, (index, component) => {
      if (_.has(components, component.types[0])) {
        components[component.types[0]] = component[options[component.types[0]]];
      }
    });

    const fullAddress = {
      address: `${components.street_number} ${components.route}`.trim(),
      city: components.locality,
      state: components.administrative_area_level_1,
      zipcode: components.postal_code,
      country: components.country,
    };
    return fullAddress;
  },

});
export default MapView;

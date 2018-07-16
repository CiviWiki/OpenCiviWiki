import { Model } from 'backbone';

const GoogleMap = Model.extend({
  defaults() {
    return {
      id: '',
      uscapitol: { lat: 38.8899389, lng: -77.0090505 },
      zoom: 5,
      coordinates: {},
      address: {},
      is_new: false,
      // Visual Setup and Initalization Options
      mapOptions: {},
      markerOptions: {},
      // Google Map Objects
      map: {},
      marker: {},
      autocomplete: {},
      geocoder: {},
    };
  },

  initialize(options) {
    if (options.coordinates) {
      this.setupMap(options.coordinates);
    } else {
      this.setupMap();
    }
  },

  setupMap(coordinates) {
    const position = coordinates || this.get('uscapitol');
    this.set('coordinates', position);

    const mapOptions = {
      // Map Placement
      zoom: this.get('zoom'),
      center: {
        lat: position.lat,
        lng: position.lng,
      },

      // Styling
      styles: [
        {
          elementType: 'labels.text.fill',
          stylers: [{ color: '#501cb5' }],
        },
        {
          featureType: 'administrative.province',
          elementType: 'geometry.stroke',
          stylers: [{ color: '#74edd6' }, { visibility: 'on' }],
        },
        {
          featureType: 'landscape',
          stylers: [{ color: '#eeeeee' }, { lightness: 75 }],
        },
        {
          featureType: 'poi.park',
          stylers: [{ visibility: 'off' }],
        },
        {
          featureType: 'road',
          stylers: [{ visibility: 'off' }],
        },
        {
          featureType: 'water',
          stylers: [{ color: '#b1b2f4' }, { visibility: 'on' }],
        },
      ],

      // Map UI Options
      disableDefaultUI: true,
      draggable: false,
      zoomControl: false,
      scrollwheel: false,
      disableDoubleClickZoom: true,
    };
    this.set('mapOptions', mapOptions);
  },

  initMapWithMarker(mapEl) {
    const googleMap = new google.maps.Map(mapEl, this.get('mapOptions'));
    this.set('map', googleMap);

    const markerOptions = {
      map: this.get('map'),
      position: this.get('coordinates'),
      icon: {
        path:
          'M18.145,0c-7.839,0-14.16,6.24-14.16,13.919C3.985,23.95,18.145,36,18.145,36s14.161-12.05,14.161-22.081 C32.306,6.24,25.984,0,18.145,0z M18.144,22.752c-0.468,0-0.925-0.047-1.374-0.117v-3.327c0.003,0,0.007,0.006,0.01,0.006 c0.083,0.003,0.24-0.144,0.24-0.144l6.743-6.242c0,0,0.118-0.125,0.121-0.195c0.003-0.079-0.128-0.227-0.128-0.227l-2.082-2.25 c0,0-0.122-0.091-0.18-0.093c-0.069-0.002-0.184,0.106-0.184,0.106l-4.082,3.777c0,0-0.182,0.259-0.276,0.256 c-0.096-0.003-0.263-0.284-0.263-0.284l-2.026-2.189c0,0-0.129-0.098-0.191-0.1c-0.074-0.003-0.196,0.12-0.196,0.12l-2.161,2.001 c0,0-0.154,0.142-0.158,0.229c-0.003,0.08,0.121,0.243,0.121,0.243l2.24,2.419l0,0l2.24,2.419c0,0,0.121,0.122,0.203,0.143v3.331 c-4.249-0.666-7.504-4.333-7.504-8.769c0-4.908,3.979-8.888,8.887-8.888c4.909,0,8.889,3.979,8.889,8.888 S23.053,22.752,18.144,22.752z', // 'M25 0c-8.284 0-15 6.656-15 14.866 0 8.211 15 35.135 15 35.135s15-26.924 15-35.135c0-8.21-6.716-14.866-15-14.866zm-.049 19.312c-2.557 0-4.629-2.055-4.629-4.588 0-2.535 2.072-4.589 4.629-4.589 2.559 0 4.631 2.054 4.631 4.589 0 2.533-2.072 4.588-4.631 4.588z',
        fillColor: '#501CB5',
        fillOpacity: 1,
        strokeColor: '',
        strokeWeight: 0,
        scaledSize: new google.maps.Size(36, 36),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(18, 36),
      },
    };
    this.set('markerOptions', markerOptions);
    this.set('marker', new google.maps.Marker(markerOptions));
    this.set('geocoder', new google.maps.Geocoder());
  },
});

export default GoogleMap;

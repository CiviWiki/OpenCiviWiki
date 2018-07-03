import { View } from 'backbone';

const MapView = View.extend({
    id: 'location',
    el: '#location',
    locationTemplate: _.template($('#location-template').html()),
    repChipTemplate: _.template($('#rep-chip-template').html()),

    events: {
        'click #browser-locate-btn': 'geolocate',
    },

    initialize: function(options) {
        options = options || {};

        this.googleMapsApiKey = options.googleMapsApiKey;
        this.sunlightApiKey = options.sunlightApiKey;
        return this;
    },

    renderAndInitMap: function(elId) {
        var _this = this;
        this.id = elId || this.id;
        this.setElement($('#' + this.id));

        if (!this.loadedAPI) {
            this.loadedAPI = true;
            var url = "https://maps.googleapis.com/maps/api/js?key=" + _this.googleMapsApiKey + "&libraries=places";
            $.ajax({
                url: url,
                dataType: "script",
                success: function(){
                    _this.render();
                }
            });
        }
    },

    render: function(){
        var viewElement = $('#' + this.id);
        this.setElement(viewElement);
        this.$el.empty().append(this.locationTemplate());
        if (typeof google != 'undefined'){
            this.model.initMapWithMarker(document.getElementById('map'));
            this.initAutocomplete();
            this.adjustMapCenter(this.model.get('coordinates'));
        }
    },

    // resizes the map to resolve grey-box sizing issues
    resizeMap: function() {
        google.maps.event.trigger(this.model.get('map'), 'resize');
        return this;
    },

    // moves the map and the marker per given coordinates
    adjustMapCenter: function(coordinates) {
        coordinates = coordinates || this.model.get('coordinates');
        this.model.set('coordinates', coordinates);
        this.model.get('map').setCenter(coordinates);
        this.model.get('marker').setPosition(coordinates);
        return this;
    },

    // Create the autocomplete input object
    initAutocomplete: function () {
        var autocomplete = new google.maps.places.Autocomplete(
            (document.getElementById('autocomplete')), {
                types: ['geocode'],
                componentRestrictions: {
                    country: 'us'
                }
        });
        autocomplete.addListener('place_changed', this.fillInAddress.bind(this));
        this.model.set('autocomplete', autocomplete);
    },

    // fillInAddress(): Get the address from the autocomplete object.
    fillInAddress: function () {
        this.$('.progress').toggleClass('hide');
        var place = this.model.get('autocomplete').getPlace();
        // Check if user didn't select any Options
        if (_.isUndefined(place.address_components)) {
            this.$('.progress').toggleClass('hide');
            return;
        }

        this.model.set('address', this.getAddressFromComponents(place.address_components));
        // Set the model's coordinates
        var coordinates = {
            lat: place.geometry.location.lat(),
            lng: place.geometry.location.lng()
        };
        this.model.set('coordinates', coordinates);
        this.model.set('is_new', true);

        this.adjustMapCenter(coordinates);
        this.$('.progress').toggleClass('hide');
    },

    // geolocate(): Use the browser's location to get coordinate values
    geolocate: function () {
        var _this = this;
        this.$('#browser-locate-btn').addClass('disabled').attr('disabled', true);
        this.$('#autocomplete').addClass('disabled').attr('disabled', true);
        this.$('.progress').removeClass('hide');
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                var geolocation = {
                    lat: Math.round(position.coords.latitude * 100000) / 100000,
                    lng: Math.round(position.coords.longitude * 100000) / 100000
                };
                if(_.isEqual(_this.model.get('coordinates'), geolocation)){
                    this.$('.progress').addClass('hide');
                    this.$('#browser-locate-btn').removeClass('disabled').attr('disabled', false);
                    this.$('#autocomplete').removeClass('disabled').attr('disabled', false);
                    return;
                }

                _this.model.set('coordinates', geolocation);

                _this.model.get('geocoder').geocode({ 'location': geolocation }, function(results, status) {
                    if (status === 'OK') {
                        _this.$('#autocomplete').val(results[0].formatted_address);
                        var fullAddress = _this.getAddressFromComponents(results[0].address_components);
                        if (fullAddress.country !== "United States") {
                            fullAddress.state = "";
                            fullAddress.zipcode = "";
                            Materialize.toast("<span>Please note that CiviWiki is optimized for the use in the U.S.</span>", 5000);
                        }
                        _this.adjustMapCenter(geolocation);
                        _this.model.set('address', fullAddress);
                        _this.model.set('is_new', true);

                    } else {
                        Materialize.toast('Geocode Error: ' + status, 2000);
                    }
                    this.$('.progress').addClass('hide');
                    this.$('#browser-locate-btn').removeClass('disabled').attr('disabled', false);
                    this.$('#autocomplete').removeClass('disabled').attr('disabled', false);

                });
            }, function(error) {
                Materialize.toast("<span>We could not use your browser's location. Please try entering your location</span>", 2000);
                this.$('.progress').addClass('hide');
                this.$('#autocomplete').removeClass('disabled').attr('disabled', false);
            });
        } else {
            Materialize.toast("<span>We could not use your browser's location. Please try entering your location</span>", 2000);
            this.$('.progress').addClass('hide');
            this.$('#autocomplete').removeClass('disabled').attr('disabled', false);
        }
    },

    getAddressFromComponents: function(address_components) {
        // Component variables we are interested in
        var components = {
            street_number: '',                  // Number
            route: '',                          // Street
            locality: '',                       // City
            administrative_area_level_1: '',    // State
            postal_code: '',                    // Zipcode
            country: ''                         // Country
        };

        var options = {
            street_number: 'long_name',                  // Number
            route: 'long_name',                          // Street
            locality: 'long_name',                       // City
            administrative_area_level_1: 'short_name',   // State
            postal_code: 'long_name',                    // Zipcode
            country: 'long_name'                         // Country
        };
        $.each(address_components, function(index, component) {
            if (_.has(components, component.types[0])) {
                components[component.types[0]]= component[options[component.types[0]]];
            }
        });

        var fullAddress = {
            address : (components.street_number + " " + components.route).trim(),
            city: components.locality,
            state: components.administrative_area_level_1,
            zipcode: components.postal_code,
            country: components.country
        };
        return fullAddress;
    },

    // SunlightAPI related functions
    getLegislators: function(coordinates){
        var _this = this;
        $.ajax({
            url: "https://congress.api.sunlightfoundation.com/legislators/locate?latitude=" + coordinates.lat + "&longitude="+ coordinates.lng + "&callback=?",
            headers:{"X-APIKEY": this.sunlightApiKey},
            dataType: "jsonp",
            success: function(data, status){
                _this.$('#rep-list').empty();
                _.each(data.results, function(rep){
                    _this.$('#rep-text').addClass('hide');
                    _this.$('#rep-list').append(_this.repChipTemplate({ rep : rep }));
                });
            },
            error: function(){
                Materialize.toast("Sunlight Error: Could not get representatives", 2000);
            }
        });
    }

});

export default MapView;
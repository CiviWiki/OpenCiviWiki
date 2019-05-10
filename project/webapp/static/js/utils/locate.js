cw = cw || {};

cw.Map = BB.Model.extend({
  defaults: function() {
    return {
      id: "",
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
      geocoder: {}
    };
  },

  initialize: function(options) {
    options = options || {};
    this.setupMap(options.coordinates);
  },

  setupMap: function(coordinates) {
    var position = coordinates || this.get("uscapitol");
    this.set("coordinates", position);

    var mapOptions = {
      // Map Placement
      zoom: this.get("zoom"),
      center: {
        lat: position.lat,
        lng: position.lng
      },

      // Styling
      styles: [
        {
          elementType: "labels.text.fill",
          stylers: [{ color: "#501cb5" }]
        },
        {
          featureType: "administrative.province",
          elementType: "geometry.stroke",
          stylers: [{ color: "#74edd6" }, { visibility: "on" }]
        },
        {
          featureType: "landscape",
          stylers: [{ color: "#eeeeee" }, { lightness: 75 }]
        },
        {
          featureType: "poi.park",
          stylers: [{ visibility: "off" }]
        },
        {
          featureType: "road",
          stylers: [{ visibility: "off" }]
        },
        {
          featureType: "water",
          stylers: [{ color: "#b1b2f4" }, { visibility: "on" }]
        }
      ],

      // Map UI Options
      disableDefaultUI: true,
      draggable: false,
      zoomControl: false,
      scrollwheel: false,
      disableDoubleClickZoom: true
    };
    this.set("mapOptions", mapOptions);
  },

  initMapWithMarker: function(mapEl) {
    var googleMap = new google.maps.Map(mapEl, this.get("mapOptions"));
    this.set("map", googleMap);

    var markerOptions = {
      map: this.get("map"),
      position: this.get("coordinates"),
      icon: {
        path:
          "M18.145,0c-7.839,0-14.16,6.24-14.16,13.919C3.985,23.95,18.145,36,18.145,36s14.161-12.05,14.161-22.081 C32.306,6.24,25.984,0,18.145,0z M18.144,22.752c-0.468,0-0.925-0.047-1.374-0.117v-3.327c0.003,0,0.007,0.006,0.01,0.006 c0.083,0.003,0.24-0.144,0.24-0.144l6.743-6.242c0,0,0.118-0.125,0.121-0.195c0.003-0.079-0.128-0.227-0.128-0.227l-2.082-2.25 c0,0-0.122-0.091-0.18-0.093c-0.069-0.002-0.184,0.106-0.184,0.106l-4.082,3.777c0,0-0.182,0.259-0.276,0.256 c-0.096-0.003-0.263-0.284-0.263-0.284l-2.026-2.189c0,0-0.129-0.098-0.191-0.1c-0.074-0.003-0.196,0.12-0.196,0.12l-2.161,2.001 c0,0-0.154,0.142-0.158,0.229c-0.003,0.08,0.121,0.243,0.121,0.243l2.24,2.419l0,0l2.24,2.419c0,0,0.121,0.122,0.203,0.143v3.331 c-4.249-0.666-7.504-4.333-7.504-8.769c0-4.908,3.979-8.888,8.887-8.888c4.909,0,8.889,3.979,8.889,8.888 S23.053,22.752,18.144,22.752z", //'M25 0c-8.284 0-15 6.656-15 14.866 0 8.211 15 35.135 15 35.135s15-26.924 15-35.135c0-8.21-6.716-14.866-15-14.866zm-.049 19.312c-2.557 0-4.629-2.055-4.629-4.588 0-2.535 2.072-4.589 4.629-4.589 2.559 0 4.631 2.054 4.631 4.589 0 2.533-2.072 4.588-4.631 4.588z',
        fillColor: "#501CB5",
        fillOpacity: 1,
        strokeColor: "",
        strokeWeight: 0,
        scaledSize: new google.maps.Size(36, 36),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(18, 36)
      }
    };
    this.set("markerOptions", markerOptions);
    this.set("marker", new google.maps.Marker(markerOptions));
    this.set("geocoder", new google.maps.Geocoder());
  }
});

cw.MapView = BB.View.extend({
  id: "location",
  el: "#location",
  locationTemplate: _.template($("#location-template").html()),
  repChipTemplate: _.template($("#rep-chip-template").html()),

  events: {
    "click #browser-locate-btn": "geolocate"
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
    this.setElement($("#" + this.id));

    if (!this.loadedAPI) {
      this.loadedAPI = true;
      var url =
        "https://maps.googleapis.com/maps/api/js?key=" +
        _this.googleMapsApiKey +
        "&libraries=places";
      $.ajax({
        url: url,
        dataType: "script",
        success: function() {
          _this.render();
        }
      });
    }
  },

  render: function() {
    var viewElement = $("#" + this.id);
    this.setElement(viewElement);
    this.$el.empty().append(this.locationTemplate());
    if (typeof google != "undefined") {
      this.model.initMapWithMarker(document.getElementById("map"));
      this.initAutocomplete();
      this.adjustMapCenter(this.model.get("coordinates"));
    }
  },

  // resizes the map to resolve grey-box sizing issues
  resizeMap: function() {
    google.maps.event.trigger(this.model.get("map"), "resize");
    return this;
  },

  // moves the map and the marker per given coordinates
  adjustMapCenter: function(coordinates) {
    coordinates = coordinates || this.model.get("coordinates");
    this.model.set("coordinates", coordinates);
    this.model.get("map").setCenter(coordinates);
    this.model.get("marker").setPosition(coordinates);
    return this;
  },

  // Create the autocomplete input object
  initAutocomplete: function() {
    var autocomplete = new google.maps.places.Autocomplete(
      document.getElementById("autocomplete"),
      {
        types: ["geocode"],
        componentRestrictions: {
          country: "us"
        }
      }
    );
    autocomplete.addListener("place_changed", this.fillInAddress.bind(this));
    this.model.set("autocomplete", autocomplete);
  },

  // fillInAddress(): Get the address from the autocomplete object.
  fillInAddress: function() {
    this.$(".progress").toggleClass("hide");
    var place = this.model.get("autocomplete").getPlace();
    // Check if user didn't select any Options
    if (_.isUndefined(place.address_components)) {
      this.$(".progress").toggleClass("hide");
      return;
    }

    this.model.set(
      "address",
      this.getAddressFromComponents(place.address_components)
    );
    // Set the model's coordinates
    var coordinates = {
      lat: place.geometry.location.lat(),
      lng: place.geometry.location.lng()
    };
    this.model.set("coordinates", coordinates);
    this.model.set("is_new", true);

    this.adjustMapCenter(coordinates);
    this.$(".progress").toggleClass("hide");
  },

  // geolocate(): Use the browser's location to get coordinate values
  geolocate: function() {
    var _this = this;
    this.$("#browser-locate-btn")
      .addClass("disabled")
      .attr("disabled", true);
    this.$("#autocomplete")
      .addClass("disabled")
      .attr("disabled", true);
    this.$(".progress").removeClass("hide");
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        function(position) {
          var geolocation = {
            lat: Math.round(position.coords.latitude * 100000) / 100000,
            lng: Math.round(position.coords.longitude * 100000) / 100000
          };
          if (_.isEqual(_this.model.get("coordinates"), geolocation)) {
            this.$(".progress").addClass("hide");
            this.$("#browser-locate-btn")
              .removeClass("disabled")
              .attr("disabled", false);
            this.$("#autocomplete")
              .removeClass("disabled")
              .attr("disabled", false);
            return;
          }

          _this.model.set("coordinates", geolocation);

          _this.model
            .get("geocoder")
            .geocode({ location: geolocation }, function(results, status) {
              var info = "";
              if (status === "OK") {
                _this.$("#autocomplete").val(results[0].formatted_address);
                var fullAddress = _this.getAddressFromComponents(
                  results[0].address_components
                );
                if (fullAddress.country !== "United States") {
                  fullAddress.state = "";
                  fullAddress.zipcode = "";
                  info =
                    "<span>Please note that CiviWiki is optimized for the use in the U.S.</span>";
                  Materialize.toast(info, 5000);
                }
                _this.adjustMapCenter(geolocation);
                _this.model.set("address", fullAddress);
                _this.model.set("is_new", true);
              } else {
                info = "Geocode Error: " + status;
                Materialize.toast(info, 2000);
              }
              this.$(".progress").addClass("hide");
              this.$("#browser-locate-btn")
                .removeClass("disabled")
                .attr("disabled", false);
              this.$("#autocomplete")
                .removeClass("disabled")
                .attr("disabled", false);
            });
        },
        function(error) {
          info =
            "<span>We could not use your browser's location. Please try entering your location</span>";
          Materialize.toast(info, 2000);
          this.$(".progress").addClass("hide");
          this.$("#autocomplete")
            .removeClass("disabled")
            .attr("disabled", false);
        }
      );
    } else {
      info =
        "<span>We could not use your browser's location. Please try entering your location</span>";
      Materialize.toast(info, 2000);
      this.$(".progress").addClass("hide");
      this.$("#autocomplete")
        .removeClass("disabled")
        .attr("disabled", false);
    }
  },

  materializeToast: function(info, duration) {
    Materialize.toast(info, duration);
  },

  getAddressFromComponents: function(address_components) {
    // Component variables we are interested in
    var components = {
      street_number: "", // Number
      route: "", // Street
      locality: "", // City
      administrative_area_level_1: "", // State
      postal_code: "", // Zipcode
      country: "" // Country
    };

    var options = {
      street_number: "long_name", // Number
      route: "long_name", // Street
      locality: "long_name", // City
      administrative_area_level_1: "short_name", // State
      postal_code: "long_name", // Zipcode
      country: "long_name" // Country
    };
    $.each(address_components, function(index, component) {
      if (_.has(components, component.types[0])) {
        components[component.types[0]] = component[options[component.types[0]]];
      }
    });

    var fullAddress = {
      address: (components.street_number + " " + components.route).trim(),
      city: components.locality,
      state: components.administrative_area_level_1,
      zipcode: components.postal_code,
      country: components.country
    };
    return fullAddress;
  },

  // SunlightAPI related functions
  getLegislators: function(coordinates) {
    var _this = this;
    $.ajax({
      url:
        "https://congress.api.sunlightfoundation.com/legislators/locate?latitude=" +
        coordinates.lat +
        "&longitude=" +
        coordinates.lng +
        "&callback=?",
      headers: { "X-APIKEY": this.sunlightApiKey },
      dataType: "jsonp",
      success: function(data, status) {
        _this.$("#rep-list").empty();
        _.each(data.results, function(rep) {
          _this.$("#rep-text").addClass("hide");
          _this.$("#rep-list").append(_this.repChipTemplate({ rep: rep }));
        });
      },
      error: function() {
        Materialize.toast(
          "Sunlight Error: Could not get representatives",
          2000
        );
      }
    });
  }
});

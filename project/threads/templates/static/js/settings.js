cw = cw || {};

cw.UserModel = BB.Model.extend({
    defaults: function() {
        return {
            username: "",
            email: "",
            location: "",
        };
    },
    url: function () {
        if (! this.get('username') ) {
            throw new Error("This is a race condition! and why we can't have nice things :(");
        }
        return '/api/account_profile/' + this.get('username') + '/';
    },

    initialize: function (model, options) {
        options = options || {};
    }
});


cw.SettingsView = BB.View.extend({

    el: '#settings',

    initialize: function(options) {
        this.options = options || {};
        this.mapView = options.mapView;

        this.template = _.template($('#settings-template').text());
        this.settingsTemplate = _.template($('#settings-base').text());
        this.personalTemplate = _.template($('#settings-personal').text());
        this.locationLabelTemplate = _.template($('#location-label').text());

        this.listenTo(this.model, 'change', this.renderAllLabels);
    },

    render: function() {
        this.$el.html(this.template());

        this.$('#settings-el').html(this.settingsTemplate());

        this.renderPersonal();

        this.mapView.renderAndInitMap();
        // var saveLocationThrottled = _.throttle(this.saveLocation, 1000);
        this.listenTo(this.mapView.model, 'change:is_new', _.bind(this.saveLocation, this));
    },

    renderAllLabels:function() {
        this.renderPersonal();
        this.renderLocationLabel();
        Materialize.updateTextFields();
    },

    renderPersonal: function() {
        this.$('#settings-1').html(this.personalTemplate());
    },

    renderLocationLabel: function() {
        this.$('#location-label-container').html(this.locationLabelTemplate());
    },

    events: {
        'blur .save-account': 'saveAccount',
    },

    saveAccount: function (e) {
        var $this = $(e.target),
            changeKey = $this.attr('id'),
            changeVal = $this.val().trim(),
            apiData = {},
            _this = this;

        if (this.model.get([changeKey]) === changeVal) {
            return;
        }

        apiData[changeKey] = changeVal;

        $.ajax({
            url: '/api/edituser/',
            type: 'POST',
            data: apiData,
            success: function () {
                Materialize.toast('Saved!', 5000);

                _this.isSave = true;
                _this.model.fetch();

            }
        });
    },

    saveLocation: function () {
        var _this = this;
        var coordinates = this.mapView.model.get('coordinates'),
            address = this.mapView.model.get('address');

        if (!this.mapView.model.get('is_new')) return;

        if (coordinates && address) {

            $.ajax({
                type: 'POST',
                url: '/api/edituser/',
                data: {
                    coordinates: coordinates,
                    address: address.address,
                    city: address.city,
                    state: address.state,
                    zip_code: address.zipcode,
                    country: address.country,
                    longitude: coordinates.lng,
                    latitude: coordinates.lat,
                },
                success: function (data) {
                    Materialize.toast('<span class="subtitle-lato white-text">Location Changed</span>', 5000);
                    _this.mapView.model.set('is_new', false);
                    _this.model.fetch();
                },
                error: function (data) {
                    if (data.status_code === 400) {
                        Materialize.toast(data.message, 5000);
                    } else if (data.status_code === 500) {
                        Materialize.toast('Internal Server Error', 5000);
                    } else {
                        Materialize.toast(data.statusText, 5000);
                    }
                }
            });
        }
    },
});

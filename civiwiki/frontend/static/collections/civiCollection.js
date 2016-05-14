var CiviCollection = Backbone.Collection.extend({

    model: CiviModel,

    initialize: function (models, options) {
        options = options || {};

        this.civiType = options.civiType;
        this.url = options.url;
    },

    parse: function (data) {
        return data.result;
    }

});

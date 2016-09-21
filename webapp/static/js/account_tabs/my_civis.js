cw = cw || {};

cw.ProfileCiviModel = BB.Model.extend({
    defaults: function() {
        return {
            type: "",
            title: "",
            body: "",
            author: "",
            ratings: [],
            attachments: [],
            date_created: ""
        };
    }
});

cw.ProfileCiviCollection = BB.Collection.extend({

    model: ProfileCiviModel,

    url: function () {
            if (! this.username ) {
                throw new Error("This is a race condition! and why we can't have nice things :(");
            }
            return '/api/getUserCivis/' + this.user_id + '/';
    },

    initialize: function (models, options) {
        options = options || {};

        this.civiType = options.civiType;
        this.url = options.url;

        this.listenTo(this.model, 'add', function () {
           console.log('something got added');
        });
    }
});

var MyCivisView = BB.View.extend({

    el: '#groups',
    groupsTemplate: _.template($('#groups-template').html()),

    initialize: function (options) {
        var _this = this;
        options = options || {};

        _this.groups = options.groups;

        var civi_list = new ProfileCiviCollection();
        civi_list.fetch({
            success: this.fetchSuccess,
            error: this.fetchError

        });

        _this.render();
    },

    render: function () {
    },

    events: {
        'click .gitem': 'permalink'
    },

    permalink: function(event) {
        var _this = this;
    },

});

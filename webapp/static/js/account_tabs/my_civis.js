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
});
//
// var Todos = new TodoList;
//
var MyCivisView = BB.View.extend({

    el: '#groups',
    groupsTemplate: _.template($('#groups-template').html()),

    initialize: function (options) {
        var _this = this;
        options = options || {};

        _this.groups = options.groups;

        var collection4 = new ProfileCiviCollection();
        collection4.fetch({
            success: this.fetchSuccess,
            error: this.fetchError

        });

        _this.render();
    },

    render: function () {
        var _this = this;
        _this.$el.empty().append(_this.groupsTemplate({
            groups: _this.sampleGroups()
            //groups: _this.groups;        // TODO: Use this when groups are available
        }));
    },

    events: {
        'click .groups-item': 'clickGroup'
    },

    // Redirects User to selected group page
    clickGroup: function(event) {
        var _this = this;
        // TODO: Link to Groups Pages once they are implemented
    },

    // Sample Data As a Placeholder
    sampleGroups: function(){
        // Assumes that each group has an id, name, and an image. Description is just added detail.
        var sample_data = [
            {id: 1, name: 'Group to protect Wild Life in Missouri Parks', description: 'We must protect nature!', image:'/static/img/team_profile/team_default.png'},
            {id: 2, name: 'WashU CompSci', description: '010101000101010101010101000010101', image:'/static/img/team_profile/team_default.png'},
            {id: 3, name: 'CiviWiki Dev Team', description: 'We love working on civiwiki!', image:'/static/img/team_profile/team_default.png'},
            {id: 4, name: 'We Complain About Everything', description: 'We hate everything!', image:'/static/img/team_profile/team_default.png'}
        ];
        return sample_data;
    }
});

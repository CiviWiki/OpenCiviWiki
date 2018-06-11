cw = cw || {};

cw.DEFAULTS = {
    types: ['problem', 'cause', 'solution'],
    types_plural: ['problems', 'causes', 'solutions'],
    civiViewStates: ['recommended', 'other'],
    viewLimit: 5,
};

cw.CiviModel = BB.Model.extend({
    defaults: function(){
        return {
            id: '', // id from server. Client id is under cid
            thread_id: '',
            type: "Civi Type",
            title: "Civi Title",
            body: "Civi Body",
            author: {
                "username": "None",
                "profile_image": "/media/profile/default.png",
                "first_name": "None",
                "last_name": "None",
            },
            votes: {
                "votes_vneg": 0,
                "votes_neg": 0,
                "votes_neutral": 0,
                "votes_pos": 0,
                "votes_vpos": 0
            },
            attachments: [],
            hashtags: [],
            created: "No Date"
        };
    },

    url: function () {
        if ( !this.id ) {
            throw new Error("This is a race condition! and why we can't have nice things :(");
        }
        return '/api/civi_data/' + this.id;
    },

    initialize: function (model, options) {
        options = options || {};
    },

    save: function(attrs, options) { // TODO: Remove this after implementing django REST framework
        options = options || {};

        options.type = 'POST';
        if (!options.url) {
            options.url = '/api/editcivi/' + this.id + '/';
        }
        return Backbone.Model.prototype.save.call(this, attrs, options);
    },

    //TODO: validate: function()

    vote: function (vote_type){

    },
});
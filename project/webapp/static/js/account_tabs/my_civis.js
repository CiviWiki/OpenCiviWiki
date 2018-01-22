cw = cw || {};

cw.ProfileCiviModel = BB.Model.extend({
    defaults: function() {
        return {
            type: "No Type",
            title: "Civi Title",
            body: "Civi Body",
            author: { "username": "None", "profile_image": "/media/profile/happy.png"},
            ratings: {"ratings": [], "total": 0, "names": ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']},
            attachments: [],
            created: "No Date"
        };
    },

    initialize: function (model, options) {
        options = options || {};
    //     this.set({
    //        ratings: r,
    //        author: a,
    //        attachments: a
    //    });
    }


});

cw.ProfileCiviCollection = BB.Collection.extend({

    model: cw.ProfileCiviModel,

    // url: function () {
    //         if (! this.username ) {
    //             throw new Error("This is a race condition! and why we can't have nice things :(");
    //         }
    //         return '/api/getUserCivis/' + this.user_id + '/';
    // },

    initialize: function (models, options) {
        options = options || {};
        this.listenTo(this.model, 'add', function () {
           console.log('a civi was added');
        });
    }
});

cw.MyCivisView = BB.View.extend({

    el: '#civis',
    mycivisTemplate: _.template($('#my-civis-template').html()),

    initialize: function (options) {
        options = options || {};

        console.log(options.civis);
        this.civis = new cw.ProfileCiviCollection({
            models: options.civis
        });
        console.log(this.civis);
        this.render();
    },

    render: function () {
        this.$el.empty().append(this.mycivisTemplate());
    },

    events: {
        'hover .gitem': 'permalink'
    },

    displayRawRating: function (event) {

    },

    permalink: function(event) {
        var _this = this;
    },

});

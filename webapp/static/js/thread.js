cw = cw || {};

cw.ThreadModel = BB.Model.extend({
    url: function () {
            if (! this.threadId ) {
                throw new Error("This is a race condition! and why we can't have nice things :(");
            }
            return '/api/thread_data/' + this.threadId + '/';
    },

    initialize: function (model, options) {
        this.threadId = options.threadId;
    }
});

cw.ThreadView = BB.View.extend({
    el: '#thread',
    template: _.template($('#thread-template').html()),
    wikiTemplate: _.template($('#thread-wiki-template').html()),
    bodyTemplate: _.template($('#thread-body-template').html()),

    initialize: function (options) {
        this.username = options.username;

        this.listenTo(this.model, 'sync', function () {
            this.wikiRender();
            this.threadBodyRender();
        });

        this.render();
    },

    render: function () {
        this.$el.empty().append(this.template());
    },

    wikiRender: function () {
        if (this.$('.thread-wiki-holder').length) {
            this.$('.thread-wiki-holder').empty().append(this.wikiTemplate());
        }
    },

    threadBodyRender: function () {
        if (this.$('.thread-body-holder').length) {
            this.$('.thread-body-holder').empty().append(this.bodyTemplate());
        }
    },

    events: {
    }

});

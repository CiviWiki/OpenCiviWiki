cw = cw || {};
cw.ThreadModel = BB.Model.extend({
    defaults: {

    },

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

cw.ResponseCollection = BB.Collection.extend({
    url: function () {
        if (! this.threadId ) {
            throw new Error("This is a race condition! and why we can't have nice things :(");
        }
        return '/api/response_data/' + this.threadId + '/' + this.civiId + '/';
    },
    initialize: function (model, options) {
        this.threadId = options.threadId;
        this.civiId = null;
    }
});

cw.FeedView = BB.View.extend({
    el: '#feed',
    template: _.template($('#feed-template').html()),

    initialize: function (options) {
        this.options = options;

        this.render();
    },

    render: function () {
        this.$el.empty().append(this.template());

        this.newThreadView = new cw.NewThreadView({
            info: this.options
        });
    },

    events: {
        'click .new-thread': 'openNewThreadModal'
    },

    openNewThreadModal: function () {
        this.newThreadView.show();
    }
});

cw.NewThreadView = BB.View.extend({
    el: '.new-thread-modal-holder',
    template: _.template($('#new-thread-template').html()),

    initialize: function (options) {
        this.options = options.info;

        this.render();
    },

    render: function () {
        this.$el.empty().append(this.template());

        cw.materializeShit();
    },

    show: function () {
        this.$('.new-thread-modal').openModal();
    },

    hide: function () {
        this.$('.new-thread-modal').closeModal();
    },

    events: {
        'click .cancel-new-thread': 'cancelThread',
        'click .create-new-thread': 'createThread'
    },

    cancelThread: function () {
        this.hide();
    },

    createThread: function () {
        var _this = this;

        var title = this.$el.find('#thread-title').val(),
            summary = this.$el.find('#thread-body').val(),
            category_id = this.$el.find('#thread-category').val();

        if (title && summary && category_id) {
            $.ajax({
                url: '/api/new_thread/',
                type: 'POST',
                data: {
                    title: title,
                    summary: summary,
                    category_id: category_id
                },
                success: function () {
                    Materialize.toast('New thread created.', 2000);
                    _this.hide();
                    _this.render();
                }
            });
        } else {
            Materialize.toast('Please input all fields.', 2000);
        }


    },
});

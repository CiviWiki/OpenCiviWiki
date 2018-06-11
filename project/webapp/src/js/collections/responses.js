cw.ResponseCollection = BB.Collection.extend({
    model: cw.CiviModel,

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
cw.ThreadModel = BB.Model.extend({
    url: function () {
        if (! this.threadId ) {
            throw new Error("This is a race condition! and why we can't have nice things :(");
        }
        return '/api/thread_data/' + this.threadId + '/';
    },

    parse: function(data){
        console.log(data);
        return data;
    },

    initialize: function (model, options) {
        this.threadId = options.threadId;
    }
});
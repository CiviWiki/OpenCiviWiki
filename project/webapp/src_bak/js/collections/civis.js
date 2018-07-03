cw.CiviCollection = BB.Collection.extend({
    model: cw.CiviModel,

    url: function () {
        if (! this.threadId ) {
            throw new Error("This is a race condition! and why we can't have nice things :(");
        }
        return '/api/threads/' + this.threadId + '/civis';
    },

    initialize: function (model, options) {
        options = options || {};
        this.threadId = options.threadId;
    },

    filterByOptions: function (options) {
        var type = options.type || 'problem';
        var viewState = options.viewState || 'default';
        var limit = options.limit || civi.length;

        var filtered = this.models.filter(function (civi) {
            return civi.get("type") === type && viewState === civi.viewState;
        });

        if (limit < civi.length && limit > 1){
            filtered = filtered.split(limit);
        }
        return filtered;
    },

    filterByType: function (type) {
        var filtered = this.models.filter(function (civi) {
            return civi.get("type") === type;
        });
        return filtered;
    },

    filterByIds: function (arrayIds) {
        var filtered = this.models.filter(function (civi) {
            return (_.indexOf(arrayIds, civi.id) > -1);
        });
        return filtered;
    },

    filterRecByType: function (type, recommended) {
        var filtered = this.models.filter(function (civi) {
            if (!recommended) {
                return (civi.get("type") === type) && civi.otherRecommended;
            }
            return (civi.get("type") === type) && (civi.recommended == recommended);
        });
        return filtered;
    },

    filterByRec: function (recommended) {
        var filtered = this.models.filter(function (civi) {
            if (!recommended) {
                return civi.otherRecommended;
            } else return (civi.recommended == recommended);

        });
        return filtered;
    },
});
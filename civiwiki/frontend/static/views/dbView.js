var TopicsCollection = Backbone.Collection.extend({

    url: 'api/topics',

    parse: function (data) {
        return data.result;
    }

});

var DatabaseView = Backbone.View.extend({

    el: '#dbview',

    categoriesTemplate: _.template($('#categories-template').html()),
    topicsTemplate: _.template($('#topics-template').html()),
    issuesTemplate: _.template($('#issues-template').html()),

    initialize: function (options) {
        options = options || {};

        this.categories = options.categories;
        this.topics = new TopicsCollection();
        this.issues = new CiviCollection([], {
            civiType: 'I',
            url: 'api/topten'
        });

        this.windowHeight = $(window).height();

        this.render();
    },

    render: function () {
        this.$el.find('.categories-holder').empty().append(this.categoriesTemplate({
            categories: this.categories.toJSON()
        }));

        this.customCSS();
    },

    customCSS: function () {
        this.$el.find('.db-list').css({
            height: this.windowHeight
        });
    },

    customRowHeight: function () {
        this.$el.find('.issues-item').css({
            height: this.windowHeight / 5
        });
    },

    events: {
        'click .categories-item': 'clickCategory',
        'click .topics-item': 'clickTopic'
    },

    clickCategory: function (e) {
        var _this = this,
            $this = $(e.target).closest('.categories-item'),
            catId = $this.attr('data-id');

        $this.siblings().removeClass('selected-category');

        this.topics.fetch({
            type: 'POST',
            data: {
                id: catId
            },
            success: function () {
                $this.addClass('selected-category');

                _this.$el.find('.topics-holder').empty().append(_this.topicsTemplate({
                    topics: _this.topics.toJSON()
                }));

                _this.customCSS();
            }
        });

    },

    clickTopic: function (e) {
        var _this = this,
            $this = $(e.target).closest('.topics-item'),
            topicId = $this.attr('data-id');

        $this.siblings().removeClass('selected-topic');

        this.issues.fetch({
            type: 'POST',
            data: {
                id: topicId
            },
            success: function () {
                $this.addClass('selected-topic');

                _this.$el.find('.issues-holder').empty().append(_this.issuesTemplate({
                    issues: _this.issues.toJSON().slice(0, 5),
                    issuesSecond: _this.issues.toJSON().slice(5, 10)
                }));

                _this.customCSS();
                _this.customRowHeight();
            }
        });
    }

});

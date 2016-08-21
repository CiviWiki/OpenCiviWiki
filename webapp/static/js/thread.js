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
            this.threadWikiRender();
        });

        this.render();
    },

    render: function () {
        this.$el.empty().append(this.template());
    },

    threadWikiRender: function () {
        if (this.$('.thread-wiki-holder').length) {
            this.$('.thread-wiki-holder').empty().append(this.wikiTemplate());

            this.threadBodyRender();
        }
    },

    threadBodyRender: function () {
        if (this.$('.thread-body-holder').length) {
            this.$('.thread-body-holder').empty().append(this.bodyTemplate());
        }
    },

    events: {
        'click .enter-body': 'scrollToBody',
        'click .enter-wiki': 'scrollToWiki',
        'click .expand-nav': 'expandNav',
        'scroll .main-thread': 'threadScroll'
    },

    scrollToBody: function () {
        this.$('.thread-body-holder').css({display: 'block'});
        $('body').css({overflow: 'hidden'});

        $('body').animate({
            scrollTop: $('.thread-body-holder').offset().top
        }, 1000);

        var $civiNavScroll = this.$('.civi-outline');
        $civiNavScroll.css({height: $('body').height() - $civiNavScroll.offset().top});
        var $civiThreadScroll = this.$('.main-thread');
        $civiThreadScroll.css({height: $('body').height() - $civiThreadScroll.offset().top});
        var $civiResponseScroll = this.$('.responses');
        $civiResponseScroll.css({height: $('body').height() - $civiResponseScroll.offset().top});
    },

    scrollToWiki: function () {
        var _this = this;

        $('body').animate({
            scrollTop: 0
        }, 1000, function () {
            _this.$('.thread-body-holder').css({display: 'none'});
        });
        $('body').css({overflow: 'scroll'});
    },

    expandNav: function (e) {
        var $this = $(e.target);

        if ($this.hasClass('expanded')) {
            $('.civi-nav-wrapper').slideUp();
            $this.removeClass('expanded');
        } else {
            $('.civi-nav-wrapper').slideDown();
            $this.addClass('expanded');
        }
    },

    threadScroll: function () {
        //TODO Change nav on scroll of main
    }

});

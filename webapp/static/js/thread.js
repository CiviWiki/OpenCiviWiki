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
        var _this = this;

        if (this.$('.thread-body-holder').length) {
            this.$('.thread-body-holder').empty().append(this.bodyTemplate());

            this.$('.main-thread').on('scroll', function (e) {
                _this.changeNavScroll(e.target.scrollTop);
            });
        }
    },

    changeNavScroll: function (scrollPosition, firstTime, navChange) {
        var _this = this;

        if (firstTime) {
            var $newNavCivi = _this.$('[data-civi-nav-id="' + _this.civiLocations[0].id + '"]');
            $newNavCivi.addClass('current');

            if (!_this.navExpanded) {
                $($newNavCivi.closest('.civi-nav-wrapper').siblings()[0]).addClass('current');
            }

            _this.currentNavCivi = _this.civiLocations[0].id;
            return;
        } else if (navChange) {
            var $currentNavCivi = _this.$('[data-civi-nav-id="' + _this.currentNavCivi + '"]');

            if (this.navExpanded) {
                $($currentNavCivi.closest('.civi-nav-wrapper').siblings()[0]).removeClass('current');
            } else {
                $($currentNavCivi.closest('.civi-nav-wrapper').siblings()[0]).addClass('current');
            }
            return;
        }

        var newCivi = _.find(_this.civiLocations, function (l) {
            return scrollPosition > l.top - 16 && scrollPosition < l.bottom + 2;
        }).id;

        if (_this.currentNavCivi !== newCivi) {
            var $currentNavCivi = _this.$('[data-civi-nav-id="' + _this.currentNavCivi + '"]'),
                $newNavCivi = _this.$('[data-civi-nav-id="' + newCivi + '"]');

            $currentNavCivi.removeClass('current');
            $newNavCivi.addClass('current');

            if (!_this.navExpanded) {
                $($currentNavCivi.closest('.civi-nav-wrapper').siblings()[0]).removeClass('current');
                $($newNavCivi.closest('.civi-nav-wrapper').siblings()[0]).addClass('current');
            }

            _this.currentNavCivi = newCivi;
            _this.currentScroll = scrollPosition;
        }
    },

    events: {
        'click .enter-body': 'scrollToBody',
        'click .enter-wiki': 'scrollToWiki',
        'click .expand-nav': 'expandNav',
        'click .civi-nav-link': 'goToCivi',
        'click .civi-header': 'drilldownCivi'
    },

    scrollToBody: function () {
        var _this = this;

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

        var threadPos = this.$('.main-thread').position().top;
        this.civiLocations = [];
        this.$('.civi-card').each(function (idx, civi) {
            var $civi = $(civi),
                $civiTop = $civi.position().top - threadPos;
            _this.civiLocations.push({top: $civiTop, bottom: $civiTop + $civi.height(), id: $civi.attr('data-civi-id')});
        });

        this.currentScroll = 0;

        _this.changeNavScroll(_this.currentScroll, true);
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
        var _this = this,
            $this = $(e.target);

        if ($this.hasClass('expanded')) {
            $('.civi-nav-wrapper').slideUp();
            $this.removeClass('expanded');
            _this.navExpanded = false;
            _this.changeNavScroll(_this.currentScroll, false, true);
        } else {
            $('.civi-nav-wrapper').slideDown();
            $this.addClass('expanded');
            _this.navExpanded = true;
            _this.changeNavScroll(_this.currentScroll, false, true);
        }
    },

    goToCivi: function (e) {
        var $link = $(e.target).closest('.civi-nav-link');
        this.$('.main-thread').animate({scrollTop: _.findWhere(this.civiLocations, {id: $link.attr('data-civi-nav-id')}).top}, 800);
    },

    drilldownCivi: function (e) {
        var $this = $(e.target);

        if (!$this.hasClass('civi-header-actions') && !$this.hasClass('material-icons')) {
            var $currentCivi = this.$('[data-civi-id="' + this.currentCivi + '"]'),
                $newCivi = $this.closest('.civi-card');

            if (this.currentCivi !== $newCivi.attr('data-civi-id')) {
                $currentCivi.removeClass('current');
                $newCivi.addClass('current');

                this.currentCivi = $newCivi.attr('data-civi-id');
                //TODO ADD RESPONSES
            } else {
                $currentCivi.removeClass('current');

                this.currentCivi = null;
                //TODO REMOVE RESPONSES
            }
        }
    }

});

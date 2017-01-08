cw = cw || {};

cw.ThreadModel = BB.Model.extend({
    url: function () {
        if (! this.threadId ) {
            throw new Error("This is a race condition! and why we can't have nice things :(");
        }
        return '/api/thread_data/' + this.threadId + '/';
    },

    parse: function(data){
        var parsed_problems = _.map(data.problems, function(c){return JSON.parse(c);});
        var parsed_causes = _.map(data.causes, function(c){return JSON.parse(c);});
        var parsed_solutions = _.map(data.solutions, function(c){return JSON.parse(c);});
        data.problems = parsed_problems;
        data.causes = parsed_causes;
        data.solutions = parsed_solutions;

        return data;
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
    //
    parse: function(data){
        var parsed_data= _.map(data, function(c){return JSON.parse(c);});
    
        return parsed_data;
    },

    initialize: function (model, options) {
        this.threadId = options.threadId;
        this.civiId = null;
    }
});

cw.NewCiviView = BB.View.extend({
    el: '.new-civi-modal-holder',
    template: _.template($('#new-civi-template').html()),

    initialize: function (options) {
        this.options = options || {};
        this.render();
    },

    render: function () {
        this.$el.empty().append(this.template());
    },

    show: function () {
        this.$('.new-civi-modal').openModal();
    },

    hide: function () {
        this.$('.new-civi-modal').closeModal();
    },

    events: {
        'click .cancel-new-civi': 'cancelCivi',
        'click .create-new-civi': 'createCivi',
        'click .civi-type-button': 'clickType'
    },

    cancelCivi: function () {
        this.hide();
    },

    createCivi: function () {
        this.hide();
        var _this = this;

        var title = this.$el.find('#civi-title').val(),
            body = this.$el.find('#civi-body').val(),
            c_type = this.$el.find('.civi-types > .current').val();

        console.log(title, body, c_type);
        if (title && body && c_type) {
            $.ajax({
                url: '/api/new_civi/',
                type: 'POST',
                data: {
                    title: title,
                    body: body,
                    c_type: c_type,
                    thread_id: this.model.threadId
                },
                success: function (response) {
                    Materialize.toast('New civi created.', 2000);
                    // var new_civi = response.data;
                    _this.model.fetch();
                    _this.options.parentView.scrollToWiki(); // HACK: this fixes big scroll, annoying? yes
                }
            });
        } else {
            Materialize.toast('Please input all fields.', 2000);
        }
    },

    clickType: function (e) {
        var $this = $(e.target).closest('.civi-type-button');

        $this.addClass('current');
        $this.siblings().removeClass('current');
    },
});

cw.NewResponseView = BB.View.extend({
    el: '.new-response-modal-holder',
    template: _.template($('#new-response-template').html()),

    initialize: function (options) {
        this.options = options || {};
        this.render();
    },

    render: function () {
        this.$el.empty().append(this.template());
    },

    events: {
        'click .create-new-response': 'createResponse',
    },

    show: function () {
        this.$('.new-response-modal').openModal();
    },

    createResponse: function () {
        var _this = this;

        var title = this.$('#response-title').val(),
            body = this.$('#response-body').val();

        if (title && body) {
            $.ajax({
                url: '/api/new_civi/',
                type: 'POST',
                data: {
                    title: title,
                    body: body,
                    c_type: 'response',
                    thread_id: this.model.threadId,
                    related_civi: this.options.parentView.currentCivi
                },
                success: function (response) {
                    Materialize.toast('New response created.', 2000);
                    // var new_civi = response.data;
                    _this.model.fetch();
                    _this.options.parentView.scrollToWiki(); // HACK: this fixes big scroll, annoying? yes
                }
            });
        } else {
            Materialize.toast('Please input all fields.', 2000);
        }
    }
});

cw.ThreadView = BB.View.extend({
    el: '#thread',
    template: _.template($('#thread-template').html()),
    wikiTemplate: _.template($('#thread-wiki-template').html()),
    bodyTemplate: _.template($('#thread-body-template').html()),
    responseWrapper: _.template($('#thread-response-template').html()),

    initialize: function (options) {
        this.username = options.username;

        this.responseCollection = new cw.ResponseCollection({}, {
            threadId: this.model.threadId
        });

        this.listenTo(this.model, 'sync', function () {
            this.threadWikiRender();
        });

        this.listenTo(this.responseCollection, 'sync', this.renderResponses);

        this.render();
    },

    render: function () {
        this.$el.empty().append(this.template());

        this.newCiviView = new cw.NewCiviView({
            model: this.model,
            parentView: this
        });

        this.newResponseView = new cw.NewResponseView({
            model: this.model,
            parentView: this
        });
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

    renderResponses: function () {
        this.$('.responses').empty().append(this.responseWrapper());
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
        'click .civi-click': 'drilldownCivi',
        'click .rating-button': 'clickRating',
        'click .favorite': 'clickFavorite',
        'click .civi-grab-link': 'grabLink',
        'click .add-civi': 'openNewCiviModal',
        'click .add-response': 'openNewResponseModal'
    },

    scrollToBody: function () {
        var _this = this;

        this.$('.thread-body-holder').css({display: 'block'});
        $('body').css({overflow: 'hidden'});

        $('body').animate({
            scrollTop: $('.thread-body-holder').offset().top
        }, 200);

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
        }, 200, function () {
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
        this.$('.main-thread').animate({scrollTop: _.findWhere(this.civiLocations, {id: $link.attr('data-civi-nav-id')}).top - 15}, 800);
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

                this.responseCollection.civiId = this.currentCivi;
                this.responseCollection.fetch();

            } else {
                $currentCivi.removeClass('current');

                this.currentCivi = null;
                this.$('.responses').empty();
            }
        }
    },

    clickRating: function (e) {
        var $this = $(e.target).closest('.rating-button');

        $this.addClass('current');
        $this.siblings().removeClass('current');
    },

    clickFavorite: function (e) {
        var $this = $(e.target);

        if ($this.text() === 'star_border') {
            $this.text('star');
        } else {
            $this.text('star_border');
        }
    },

    grabLink: function () {
        Materialize.toast('Civi link copied to clipboard.', 1500);
    },

    openNewCiviModal: function () {
        this.newCiviView.show();
    },

    openNewResponseModal: function () {
        this.newResponseView.show();
    }

});

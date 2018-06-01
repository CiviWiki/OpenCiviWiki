cw.ThreadView = BB.View.extend({
    el: '#thread',
    template: _.template($('#thread-template').html()),
    wikiTemplate: _.template($('#thread-wiki-template').html()),
    bodyTemplate: _.template($('#thread-body-template').html()),
    responseWrapper: _.template($('#thread-response-template').html()),
    outlineTemplate: _.template($('#outline-template').html()),

    initialize: function (options) {
        options = options || {};
        this.username = options.username;
        this.civis = options.civis;
        this.navExpanded = true;
        this.is_draft = options.is_draft;

        this.civiRecViewLimits = {problem : 0,cause: 0,solution: 0};
        this.civiOtherViewLimits = {problem : 0,cause: 0,solution: 0};
        this.civiRecViewTotals = {problem : 0,cause: 0,solution: 0};
        this.civiOtherViewTotals = {problem : 0,cause: 0,solution: 0};

        this.viewRecommended = true;
        this.recommendedCivis = [];
        this.otherCivis = [];
        this.outlineCivis = {};
        this.initRecommended();

        this.responseCollection = new cw.ResponseCollection({}, {
            threadId: this.model.threadId
        });

        this.listenTo(this.responseCollection, 'sync', this.renderResponses);
        this.render();
    },

    initRecommended: function() {
        var _this = this;
        this.recommendedCivis = [];
        this.otherCivis = [];
        this.civiRecViewTotals = {problem : 0,cause: 0,solution: 0};
        this.civiOtherViewTotals = {problem : 0,cause: 0,solution: 0};

        var civiRecViewLimits= {problem : 0,cause: 0,solution: 0},
        civiOtherViewLimits= {problem : 0,cause: 0,solution: 0};
        // 1. Get id list of voted civis\
        var votes = this.model.get('user_votes');

        if (this.is_draft) {
            _.each(this.civis.models, function(civi){
                this.recommendedCivis.push(civi.id);
            }, this);
        } else {
            _.each(this.civis.models, function(civi){
                var voteData = _.findWhere(votes, {civi_id: civi.id});
                if (!_.isUndefined(voteData)) {

                    civi.voted = true;
                    var type = civi.get('type');
                    if (type === 'problem') {
                        civiRecViewLimits[type]++;
                        civiOtherViewLimits[type]++;
                    } else if (voteData.activity_type == 'vote_pos' || voteData.activity_type == 'vote_vpos') {
                        civiRecViewLimits[type]++;
                    } else {
                        civiOtherViewLimits[type]++;
                    }

                    if ((voteData.activity_type == 'vote_pos' || voteData.activity_type == 'vote_vpos')){
                        _.each(civi.get('links'), function(link){
                            var linked_civi = this.civis.get(link);
                            if (linked_civi) {
                                this.recommendedCivis.push(link);
                            }
                        }, this);
                    } else {
                        _.each(civi.get('links'), function(link){
                            var linked_civi = this.civis.get(link);
                            if (linked_civi) {
                                this.otherCivis.push(link);
                            }
                        }, this);
                    }
                } else {
                    civi.voted = false;
                }
            }, this);
        }


        // Recommended civis pool takes precedence
        this.otherCivis = _.difference(this.otherCivis, this.recommendedCivis);

        _.each(this.civis.filterByType('problem'), function(civi){
            this.recommendedCivis.push(civi.id);
            this.otherCivis.push(civi.id);
        },this);

        _.each(cw.DEFAULTS.types, function(type){
            if (this.civiRecViewLimits[type] === 0) {
                if (civiRecViewLimits[type] < 5) {
                    civiRecViewLimits[type] = 5;
                }
                this.civiRecViewLimits[type] = civiRecViewLimits[type];
            }
            if (this.civiOtherViewLimits[type] === 0) {
                if (civiOtherViewLimits[type] < 5) {
                    civiOtherViewLimits[type] = 5;
                }
                this.civiOtherViewLimits[type] = civiOtherViewLimits[type];
            }



        }, this);




    },

    render: function () {
        this.$el.empty().append(this.template());

        this.editThreadView = new cw.EditThreadView({
            model: this.model,
            parentView: this,
            threadId: this.model.threadId
        });

        this.$('.thread-wiki-holder').addClass('hide');

        this.threadWikiRender();
        this.threadBodyRender();

        // this.$('.scroll-col').height($(window).sheight() - this.$('.body-banner').height());


        this.newCiviView = new cw.NewCiviView({
            model: this.model,
            parentView: this
        });


        this.renderBodyContents();
        this.scrollToBody();

    },

    threadWikiRender: function () {
        if (this.$('.thread-wiki-holder').length) {
            this.$('.thread-wiki-holder').empty().append(this.wikiTemplate());
        }
    },

    threadBodyRender: function () {
        var _this = this;

        if (this.$('.thread-body-holder').length) {
            var bodyRenderData = {
                is_draft: this.is_draft,
            };
            this.$('.thread-body-holder').empty().append(this.bodyTemplate(bodyRenderData));

            this.$('.main-thread').on('scroll', function (e) {
                _this.processCiviScroll();
            });
        }
    },

    renderBodyContents: function () {
        this.renderCivis();
        this.renderOutline();

        if (!this.is_draft) {
            this.renderVotes();
        }
    },

    renderOutline: function(){
        var _this = this;
        if (this.civis.length === 0){
            this.$('#civi-outline').empty().append(this.outlineTemplate());
        }

        // Render Outline Template based on models
        var problems = this.outlineCivis.problem;
            causes = this.outlineCivis.cause;
            solutions = this.outlineCivis.solution;

        var renderData = {
            problems: problems,
            causes: causes,
            solutions: solutions
        };

        var recCount = { problem:0, cause:0, solution:0};
        var otherCount = { problem:0, cause:0, solution:0};
        var votes = this.model.get('user_votes'),
            voteIds = _.pluck(votes, 'civi_id');

        var counterCount = 0;
        _.each(_this.civis.models, function(c){
            var type = c.get('type');
            if (_.indexOf(voteIds, c.id) > -1) {
                // If part of current view setting
                if (_.indexOf(_this.recommendedCivis, c.id) > -1) {
                    recCount[type]++;
                } else if (_.indexOf(_this.otherCivis, c.id) > -1){
                    otherCount[type]++;
                }
            }
        });

        var highlightCount = {problem: 0,cause: 0,solution: 0};
        _.each(cw.DEFAULTS.types, function(type) {
            if (_this.viewRecommended){
                highlightCount[type] = _this.civiRecViewTotals[type];
            } else {
                highlightCount[type] = _this.civiOtherViewTotals[type];
            }
        });
        var voteCount, totalRec, totalOther;
        if (this.viewRecommended){
            voteCount = recCount;
        } else {
            voteCount = otherCount;
        }

        var count;
        if (this.is_draft) {
            count = {
                problem: highlightCount.problem,
                cause: highlightCount.cause,
                solution: highlightCount.solution,
            };
        } else {
            count = {
                problem: highlightCount.problem - recCount.problem,
                cause: highlightCount.cause - voteCount.cause,
                solution: highlightCount.solution - voteCount.solution,
            };
        }


        count.totalRec = this.civiRecViewTotals.problem + this.civiRecViewTotals.cause + this.civiRecViewTotals.solution - recCount.problem - recCount.cause - recCount.solution;
        count.totalOther = this.civiOtherViewTotals.problem + this.civiOtherViewTotals.cause + this.civiOtherViewTotals.solution - recCount.problem - otherCount.cause - otherCount.solution;

        renderData.count = count;
        renderData.is_draft = this.is_draft;

        this.$('#civi-outline').empty().append(this.outlineTemplate(renderData));
        this.$('#recommended-switch').attr('checked', this.viewRecommended);

        if (this.viewRecommended){
            this.$(".label-recommended").addClass('current');
            this.$(".label-other").removeClass('current');
            this.$(".badge-recommended").addClass('current');
            this.$(".badge-other").removeClass('current');
            this.$(".civi-nav-count").removeClass('other');
        } else {
            this.$(".label-recommended").removeClass('current');
            this.$(".label-other").addClass('current');
            this.$(".badge-recommended").removeClass('current');
            this.$(".badge-other").addClass('current');
            this.$(".civi-nav-count").addClass('other');
        }
        // view more

        _.each(cw.DEFAULTS.types, function(type) {
            var loadMore = this.$('#thread-'+type+'s>.' + type + '-loader');
            if (loadMore) {
                loadMore.clone().appendTo('#'+type+'-nav');
            }
        }, this);

        // Calculate tracking
        this.calcCiviLocations();
        // Padding so you can scroll and track the last civi element;
        var scrollPadding = this.$('.main-thread').height() - this.civiLocations[this.civiLocations.length-1].height;
        this.$('.civi-padding').height(scrollPadding - 8);

        // Vote indication
        var outline = this.$('#civi-outline');
        _.each(this.model.get('user_votes'), function(v){
            // var navItem = outline.find('#civi-nav-'+ v.civi_id);
            // navItem.before('<i class="material-icons tiny voted">beenhere</i>').addClass('nav-inactive');
            outline.find('#civi-nav-'+ v.civi_id).addClass('nav-inactive');
            var navItemState = outline.find('#civi-nav-state-' + v.civi_id);
            navItemState.addClass('voted').text('beenhere');
        }, this);



        this.expandNav();
    },

    renderCivis: function () {
        this.$('#thread-problems').empty();
        this.$('#thread-causes').empty();
        this.$('#thread-solutions').empty();

        this.threadCivis = {};
        _.each(['problem', 'cause', 'solution'], function(type){
            var civis = this.civis.filterByType(type);
            // Filter by Recommended state if not 'problem' type
            var recCivis = _.filter(civis, function(c) {
                return (_.indexOf(this.recommendedCivis, c.id) != -1);
            }, this);
            this.civiRecViewTotals[type] = recCivis.length;
            var otherCivis = _.filter(civis, function(c) {
                return (_.indexOf(this.otherCivis, c.id) != -1);
            }, this);
            this.civiOtherViewTotals[type] = otherCivis.length;
            if (type != 'problem') {
                if (this.viewRecommended) {
                    civis =recCivis;
                } else {
                    civis =otherCivis;
                }
            }
            // Sort civi list by score
            civis = _.sortBy(civis, function(civi){
                if (civi.voted) {
                    return -civi.get('score') - 100;
                }
                return -civi.get('score');
            });

            // Cut by type view limit TODO: move to rendering

            var limit;
            if (this.viewRecommended) {
                limit = this.civiRecViewLimits[type];
            } else {
                limit = this.civiOtherViewLimits[type];
            }
            var totalCount = civis.length;

            if(totalCount > limit && !this.is_draft) {
                civis = civis.slice(0,limit);
                _.each(civis, this.civiRenderHelper, this);
                this.$('#thread-'+type+'s').append('<div class="'+type+'-loader civi-load-more"><span class="civi-show-count">'+limit+'/'+totalCount+ ' '+ type+'s</span> <span class="btn-loadmore" data-civi-type="'+type+'">View More +</span></div>');
            } else {
                _.each(civis, this.civiRenderHelper, this);
            }

            this.outlineCivis[type] = civis;

        }, this);



        // _.each(this.civis.filterByType('cause'), this.civiRenderHelper, this);
        // _.each(this.civis.filterByType('solution'), this.civiRenderHelper, this);
    },

    civiRenderHelper: function(civi){
        var is_draft = this.is_draft;
        var can_edit = civi.get('author').username == this.username ? true : false;
        this.$('#thread-'+civi.get('type')+'s').append(new cw.CiviView({model: civi, can_edit: can_edit, is_draft: is_draft, parentView: this}).el);

    },

    renderVotes: function() {
        var _this = this;
        var savedVotes = this.model.get('user_votes');
        _.each(savedVotes, function(v){
            this.$('#civi-'+ v.civi_id).find("." +v.activity_type).addClass('current');
        });

        // // Indicate vote status on nav
        // _.each(['problem', 'cause', 'solution'], function(type){
        //     if (this[type+'s'].length === 0) {
        //         this.$('.' + type + '-nav>.civi-nav-header').addClass('nav-inactive');
        //     }
        // }, this);
    },

    renderResponses: function () {
        this.$('.responses-box').empty().append(this.responseWrapper());
        this.newResponseView = new cw.NewResponseView({
            model: this.model,
            parentView: this
        });


        _.each(this.responseCollection.models, function(civi){
            var can_edit = civi.get('author').username == this.username ? true : false;
            var can_respond = this.civis.get(this.responseCollection.civiId).get('author').username == this.username ? true : false;

            var new_civi_view = new cw.CiviView({model: civi, can_edit: can_edit, can_respond: can_respond, parentView: this, response: true});
            this.$('#response-list').append(new_civi_view.el);

            var vote = _.find(this.model.get('user_votes'), function(v){
                return v.civi_id === civi.id;
            });
            if (vote) {
                this.$('#civi-'+ vote.civi_id).find("." +vote.activity_type).addClass('current');
            }
            if (civi.get('rebuttal')) {
                var rebuttal_model = new cw.CiviModel(civi.get('rebuttal'));
                var rebuttal_can_edit = rebuttal_model.get('author').username == this.username ? true : false;
                var rebuttal_view = new cw.CiviView({model: rebuttal_model, can_edit: rebuttal_can_edit, can_respond: false, parentView: this, response: true});
                rebuttal_view.$('.civi-card').addClass('push-right');
                new_civi_view.el.after(rebuttal_view.el);

                vote = _.find(this.model.get('user_votes'), function(v){
                    return v.civi_id === rebuttal_model.id;
                });
                if (vote) {
                    this.$('#civi-'+ vote.civi_id).find("." +vote.activity_type).addClass('current');
                }
            }
        }, this);

        // add padding
        var $lastResponseCivi = this.$('#response-list div:last-child');
        var scrollPadding = this.$('.responses').height() - $lastResponseCivi.height();
        this.$('.responses-padding').height(scrollPadding - 8);
    },

    events: {
        'click .enter-body': 'scrollToBody',
        'click .enter-wiki': 'scrollToWiki',
        'click .expand-nav': 'toggleExpandNav',
        'click .civi-nav-link': 'goToCivi',
        'click .civi-card': 'drilldownCivi',
        'click .add-civi': 'openNewCiviModal',
        'click .add-response': 'openNewResponseModal',
        'click #recommended-switch': 'toggleRecommended',
        'click .btn-loadmore': 'loadMoreCivis',
        'click .edit-thread-button': 'openEditThreadModal',
        'click #js-publish-btn': 'publishThread'
    },

    scrollToBody: function () {
        var _this = this;

        this.$('.thread-wiki-holder').addClass('hide');
        this.$('.thread-body-holder').removeClass('hide');
        this.$('.thread-body-holder').css({display: 'block'});

        this.resizeBodyToWindow();

        this.renderOutline();
        this.processCiviScroll();
    },

    resizeBodyToWindow: function() {
        $('body').css({overflow: 'hidden'});

        var $windowHeight = $('body').height();
        var bodyHeight = $windowHeight - $("#js-global-nav").height();

        var $civiNavScroll = this.$('.civi-outline');
        $civiNavScroll.css({height: $windowHeight - $civiNavScroll.offset().top});
        var $civiThreadScroll = this.$('.main-thread');
        $civiThreadScroll.css({height: $windowHeight - $civiThreadScroll.offset().top});
        var $civiResponseScroll = this.$('.responses');
        $civiResponseScroll.css({height: $windowHeight - $civiResponseScroll.offset().top});
    },

    scrollToWiki: function () {
        var _this = this;

        this.$('.thread-body-holder').addClass('hide');
        this.$('.thread-wiki-holder').removeClass('hide');
        $('body').css({overflow: 'scroll'});
    },

    toggleExpandNav: function(e) {
        this.navExpanded = !this.navExpanded;
        this.expandNav(e);
    },

    expandNav: function (e) {
        var _this = this,
            $this = _.isUndefined(e) ? this.$('.expand-nav') : $(e.target);

        if (!this.navExpanded) {
            $('.civi-nav-wrapper').hide();
            $this.removeClass('expanded');
        } else {
            $('.civi-nav-wrapper').show();
            $this.addClass('expanded');
        }
        this.activateNav();
    },

    goToCivi: function (e) {
        var $link = $(e.target).closest('.civi-nav-link');
        this.$('.main-thread').animate({scrollTop: _.findWhere(this.civiLocations, {id: $link.attr('data-civi-nav-id')}).top - 15}, 250);
    },

    calcCiviLocations: function(){
        var _this = this;
        var threadPos = this.$('.main-thread').position().top;
        var scrollPos = this.$('.main-thread').scrollTop();
        this.civiLocations = [];
        // this.civiTops = [];
        // this.civiTargets =
        this.$('.civi-card').each(function (idx, civi) {
            var $civi = $(civi),
                $civiTop = $civi.position().top + scrollPos - threadPos;
            _this.civiLocations.push({top: $civiTop, bottom: $civiTop + $civi.height(), height: $civi.height(), target: $civi, id: $civi.attr('data-civi-id')});
            // _this.civiTops.push($civiTop);
            // _this.civiTargets.push({top: $civiTop, target: $civi, id: $civi.data('civi-id') });
        });
    },

    processCiviScroll: function () {
        var _this = this;
        var scrollPosition = this.$('.main-thread').scrollTop();
        // 1. Check if there are any civis. No tracking if none
        if (this.civis.length === 0){
            return;
        }

        // TODO: check if nav is folded, then just p-c-solution check
        //
        // if (firstTime) {
        //     var $newNavCivi = _this.$('[data-civi-nav-id="' + _this.civiLocations[0].id + '"]');
        //     $newNavCivi.addClass('current');
        //
        //     if (!_this.navExpanded) {
        //         $($newNavCivi.closest('.civi-nav-wrapper').siblings()[0]).addClass('current');
        //     }
        //
        //     _this.currentNavCivi = _this.civiLocations[0].id;
        //     return;
        // } else
        // if (navChange) {
        //     var $currentNavCivi = _this.$('[data-civi-nav-id="' + _this.currentNavCivi + '"]');
        //
        //     if (this.navExpanded) {
        //         $($currentNavCivi.closest('.civi-nav-wrapper').siblings()[0]).removeClass('current');
        //     } else {
        //         $($currentNavCivi.closest('.civi-nav-wrapper').siblings()[0]).addClass('current');
        //     }
        //     return;
        // }
        // 2. Go through list of heights to get current active civi
        var OFFSET = 100;
        var element = _.find(this.civiLocations, function (l) {
            return this.currentNavCivi !== l.id &&
                scrollPosition >= l.top - OFFSET &&
                scrollPosition < l.bottom - OFFSET;
        }, this);
        // 3. Activate Corresponding Civi Card and Nav
        if (!element) return;
        else {
            this.activateNav(element.id);
            this.autoscrollCivi(this.$('#civi-'+ element.id));
        }

    },

    activateNav: function(id) {
        var _this = this;
        this.currentNavCivi = id || this.currentNavCivi;
        var $currentNavCivi = _this.$('[data-civi-nav-id="' + _this.currentNavCivi + '"]');
            // $newNavCivi = _this.$('[data-civi-nav-id="' + newCivi + '"]');


        // $newNavCivi.addClass('current');
        if (!_this.navExpanded) {
            this.$('.civi-nav-header').removeClass('current');
            $($currentNavCivi.closest('.civi-nav-wrapper').siblings()[0]).addClass('current');
        } else {
            this.$('.civi-nav-link').removeClass('current');
            this.$('.civi-nav-header').removeClass('current');
            $currentNavCivi.addClass('current');
        }

    },

    autoscrollCivi: function (target) {
        // TODO: Throttle may need to be somewhere else
        var $this = target;

        var $currentCivi = this.$('[data-civi-id="' + this.currentCivi + '"]'),
            $newCivi = $this.closest('.civi-card');

        if (this.currentCivi !== $newCivi.attr('data-civi-id')) {
            // $currentCivi.removeClass('current');
            this.$('.civi-card').removeClass('current');
            $newCivi.addClass('current');
            var civi_id = $newCivi.data('civi-id');

            // var links = this.civis.get(civi_id).get('links');
            // // var links_related = [];
            // // _.each(links, function(link){
            // //     links_related = this.$('#civi-'+link).data('civi-links');
            // //     console.log(links_related);
            // //     if (!links_related) return;
            // //     if (links_related.length > 1){
            // //         links_related= links_related.split(",").map(Number);
            // //     } else {
            // //         links_related = parseInt(links_related);
            // //     }
            // //
            // //     links = _.union(links, links_related);
            // // },this);
            // // console.log(links);
            //
            // _.each(this.$('.civi-card'), function(civiCard){
            //     // console.log(links, $(civiCard).data('civi-id'));
            //
            //     if (links.indexOf($(civiCard).data('civi-id')) == -1 ){
            //         $(civiCard).removeClass('linked');
            //     } else {
            //         $(civiCard).addClass('linked');
            //     }
            // });

            this.currentCivi = $newCivi.attr('data-civi-id');
            if (!_.isUndefined(this.currentCivi)){
                this.responseCollection.civiId = this.currentCivi;
                this.responseCollection.fetch();
            }


        } else {
            $currentCivi.removeClass('current');
            this.$('.civi-card').removeClass('linked');

            this.currentCivi = null;
            this.$('.responses-box').empty();
        }

    },

    drilldownCivi: function (e) {
        var target = $(e.target);
        var ms_check = target.hasClass('ms-ctn') || target.hasClass('ms-sel-ctn') || target.hasClass('ms-close-btn') || target.hasClass('ms-trigger') || target.hasClass('ms-trigger-ico') || target.hasClass('ms-res-ctn') || target.hasClass('ms-sel-item') || target.hasClass('ms-res-group');

        if (target.hasClass('btn') || target.hasClass('rating-button') || target.is('input') || target.is('textarea') || target.is('label') || target.hasClass('input') || ms_check) {
            return;
        }
        var $this = $(e.currentTarget);
        if ($this.find('.civi-type').text() != "response" && $this.find('.civi-type').text() != "rebuttal") {
            var $currentCivi = this.$('[data-civi-id="' + this.currentCivi + '"]'),
                $newCivi = $this.closest('.civi-card');

            if (this.currentCivi !== $newCivi.attr('data-civi-id')) {
                // $currentCivi.removeClass('current');
                this.$('.civi-card').removeClass('current');
                $newCivi.addClass('current');
                var civi_id = $newCivi.data('civi-id');

                this.currentCivi = $newCivi.attr('data-civi-id');

                this.responseCollection.civiId = this.currentCivi;
                this.responseCollection.fetch();

            } else {
                $currentCivi.removeClass('current');
                this.$('.civi-card').removeClass('linked');

                this.currentCivi = null;
                this.$('.responses-box').empty();
            }
        }
    },

    selectInitialCiviAfterToggle: function(){
        var $newCivi = this.$('.civi-card').first();

        $newCivi.addClass('current');
        this.currentCivi = $newCivi.attr('data-civi-id');

        this.responseCollection.civiId = this.currentCivi;
        this.responseCollection.fetch();

    },

    loadMoreCivis: function(e) {
        var $target = $(e.currentTarget);
        var type = $target.data('civi-type');
        var limit, remaining;
        if (this.viewRecommended) {
            limit = this.civiRecViewLimits[type];
            remaining =  this.civiRecViewTotals[type] - limit;
        } else {
            limit = this.civiOtherViewLimits[type];
            remaining =  this.civiOtherViewTotals[type] - limit;
        }
        if (remaining <= 0) {
            return;
        }
        var addCount = (cw.DEFAULTS.viewLimit < remaining ? cw.DEFAULTS.viewLimit : remaining);

        if (this.viewRecommended) {
            this.civiRecViewLimits[type] += addCount;
        } else {
            this.civiOtherViewLimits[type] += addCount;
        }
        this.renderBodyContents();
    },

    toggleRecommended: function(e) {
        var target = $(e.currentTarget);
        var recommend_state = target.is(":checked");

        this.viewRecommended = recommend_state;

        this.$('.main-thread').scrollTop(0);
        this.renderBodyContents();
        this.processCiviScroll();
        this.selectInitialCiviAfterToggle();
    },

    publishThread: function(e){
        var _this = this;
        _this.$(e.currentTarget).addClass('disabled').attr('disabled', true);

        $.ajax({
            url: '/api/edit_thread/',
            type: 'POST',
            data: {
                thread_id: _this.model.threadId,
                is_draft: false,
            },
            success: function (response) {
                _this.is_draft = false
                Materialize.toast('Thread is now public. Refreshing the page...', 5000);
                _this.$("#js-publish-btn").hide()
                var reload_page = _.bind(location.reload, location);
                _.delay(reload_page, 1000);
            },
            error: function (response) {
                if (response.status === 403) {
                    Materialize.toast('You do not have permission to publish the thread', 5000);
                }
                else if (response.status === 500) {
                    Materialize.toast('Server Error: Thread could not be published', 5000);
                    _this.$(e.currentTarget).removeClass('disabled').attr('disabled', false);
                }
            }
        });
    },

    openNewCiviModal: function () {
        this.newCiviView.render();
    },

    openNewResponseModal: function () {
        this.newResponseView.render();
    },

    openEditThreadModal: function() {
        this.editThreadView.render();
    },

    assign: function(view, selector) {
        view.setElement(this.$(selector)).render();
    }
});

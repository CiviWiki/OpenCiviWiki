cw = cw || {};

cw.CiviModel = BB.Model.extend({
    defaults: function(){
        return {
            id: '', //id from server. Client id is under cid
            thread_id: '',
            type: "Civi Type",
            title: "Civi Title",
            body: "Civi Body",
            author: {
                "username": "None",
                "profile_image": "/media/profile/default.png",
                "first_name": "None",
                "last_name": "None",
            },
            votes: {
                "votes_vneg": 0,
                "votes_neg": 0,
                "votes_neutral": 0,
                "votes_pos": 0,
                "votes_vpos": 0
            },
            attachments: [],
            hashtags: [],
            created: "No Date"
        };
    },

    url: function () {
        if ( !this.id ) {
            throw new Error("This is a race condition! and why we can't have nice things :(");
        }
        return '/api/civi_data/' + this.id;
    },

    initialize: function (model, options) {
        options = options || {};
    },

    save: function(attrs, options) { // TODO: Remove this after implementing django REST framework
        options = options || {};

        options.type = 'POST';
        if (!options.url) {
            options.url = '/api/editcivi/' + this.id + '/';
        }
        return Backbone.Model.prototype.save.call(this, attrs, options);
    },

    //TODO: validate: function()

    vote: function (vote_type){

    },
});

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

cw.CiviSubCollection = BB.Collection.extend({
    model: cw.CiviModel,
    comparator: function(model) {
        return -model.get('score');
    },

    initialize: function (options) {
        options = options || {};
    },

});

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

cw.CiviView =  BB.View.extend({
    template: _.template($('#civi-template').html()),

    initialize: function (options) {
        this.options = options || {};
        this.can_edit = options.can_edit;
        this.parentView = options.parentView;
        this.civis = this.parentView.civis;
        this.model.set('view', this);
        this.render();
    },

    render: function () {
        this.$el.empty().append(this.template());
    },

    events: {
        'click .rating-button': 'clickRating',
        // 'click .favorite': 'clickFavorite',
        'click .edit': 'clickEdit',
        'click .delete': 'deleteEdit',
        'click .edit-confirm': 'saveEdit',
        'click .edit-cancel': 'closeEdit',
        // 'click .civi-grab-link': 'grabLink',
        // vote
        // changevote

    },
    // clean() function
    clickFavorite: function (e) {
        var _this = this;

        if ($this.text() === 'star_border') {
            $.ajax({
                url: '/api/favorite_civi/',
                type: 'POST',
                data: {
                    civi_id: this.model.id,
                },
                success: function (response) {
                    Materialize.toast('Favorited Civi', 2000);
                    $this.text('star');
                },
                error: function(r){
                    Materialize.toast('Could not favor the civi', 2000);
                }
            });

        } else {
            $.ajax({
                url: '/api/favorite_civi/',
                type: 'POST',
                data: {
                    civi_id: this.model.id,
                },
                success: function (response) {
                    Materialize.toast('Favorited Civi', 2000);
                },
                error: function(r){
                    Materialize.toast('Could not favor the civi', 2000);
                }
            });
            $this.text('star_border');
        }
    },

    grabLink: function () {
        e.stopPropagation();
        Materialize.toast('Civi link copied to clipboard.', 1500);
    },

    clickRating: function (e) {
        e.stopPropagation();
        var _this = this;
        var $this = $(e.currentTarget);

        var rating = $this.data('rating');
        var civi_id = $(e.currentTarget).closest('.civi-card').data('civi-id');

        // if (this.can_edit) {
        //     Materialize.toast('Trying to vote on your own civi? :}', 2000);
        //     return;
        // }
        if (rating && civi_id){
            $.ajax({
                url: '/api/rate_civi/',
                type: 'POST',
                data: {
                    civi_id: civi_id,
                    rating: rating
                },
                success: function (response) {
                    Materialize.toast('Voted!', 2000);
                    // var score = $this.find('.rate-value');
                    // var new_vote = parseInt(score.text())+ 1;
                    // score.text(new_vote);
                    console.log(response.data);
                    var prev_votes = _this.parentView.model.get('user_votes');
                    var prev_vote = _.findWhere(prev_votes, {civi_id: civi_id});
                    if (!prev_vote) {
                        prev_votes.push(response.data);
                        _this.parentView.model.set('user_votes', prev_votes);
                    } else {
                        prev_votes = _.reject(prev_votes, function(v) {return v.civi_id === civi_id;});
                        prev_votes.push(response.data);
                        _this.parentView.model.set('user_votes', prev_votes);
                    }

                    _this.parentView.initRecommended();
                    _this.parentView.renderBodyContents();
                    _this.parentView.processCiviScroll();

                    _this.$('.rating-button').removeClass('current');
                    $this.addClass('current');
                },
                error: function(r){
                    Materialize.toast('Could not vote :(', 2000);
                }
            });
        }
    },

    clickEdit: function (e) {
        e.stopPropagation();
        this.$('.edit-civi-body').text(this.model.get('body'));
        this.$('.edit-civi-title').val(this.model.get('title'));
        this.magicSuggestView = new cw.LinkSelectView({$el: this.$('#magicsuggest-'+this.model.id), civis: this.civis});
        this.magicSuggestView.setLinkableData(this.model.get('type'));
        this.magicSuggestView.ms.setValue(this.model.get('links'));

        this.$('.edit-wrapper').removeClass('hide');
        this.$('.edit-action').removeClass('hide');
        this.$('.text-wrapper').addClass('hide');
        this.$('.edit').addClass('hide');
        this.$('.delete').addClass('hide');
    },

    closeEdit: function (e) {
        e.stopPropagation();
        this.$('.edit-wrapper').addClass('hide');
        this.$('.edit-action').addClass('hide');
        this.$('.text-wrapper').removeClass('hide');
        this.$('.edit').removeClass('hide');
        this.$('.delete').removeClass('hide');
    },

    saveEdit: function(e) {
        e.stopPropagation();
        var _this = this;

        var new_body = this.$('.edit-civi-body').val().trim();
            new_title = this.$('.edit-civi-title').val().trim();
        var links = this.magicSuggestView.ms.getValue();
        console.log(_.isEqual(links, this.model.get('links')));
        if (!new_body || !new_title){
            Materialize.toast('Please do not leave fields blank', 2000);
            return;
        } else if ((new_body == this.model.get('body') && new_title == this.model.get('title') && _.isEqual(links, this.model.get('links')) )){
            this.closeEdit(e);
            return;
        } else {
            $.ajax({
                url: '/api/edit_civi/',
                type: 'POST',
                data: {
                    civi_id: this.model.id,
                    title: new_title,
                    body: new_body,
                    links: links
                },
                success: function (response) {
                    Materialize.toast('Saved!', 2000);
                    // var score = $this.find('.rate-value');
                    // var new_vote = parseInt(score.text())+ 1;
                    // score.text(new_vote);
                    _this.model.set('title', new_title);
                    _this.model.set('body', new_body);
                    _this.model.set('links', links);
                    _this.render();
                    _this.parentView.renderOutline();
                },
                error: function(r){
                    Materialize.toast('Could not edit the civi', 2000);
                    _this.closeEdit(e);
                }
            });
        }
    },

    deleteEdit: function(e) {
        var _this = this;
        e.stopPropagation();
        $.ajax({
            url: '/api/delete_civi/',
            type: 'POST',
            data: {
                civi_id: this.model.id,
            },
            success: function (response) {
                Materialize.toast('Deleted Civi succssfully', 2000);
                _.each(_this.model.links, function(link){
                    _this.civis.findWhere({id: link}).view.render();
                });

                _this.civis.remove(_this.model);
                _this.remove();
                _this.parentView.renderOutline();

            },
            error: function(r){
                Materialize.toast('Could not delete the civi', 2000);
            }
        });
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
        this.magicSuggestView = new cw.LinkSelectView({$el: this.$('#magicsuggest'), civis: this.options.parentView.civis});
        // this.renderMagicSuggest();
    },

    // renderMagicSuggest: function() {
    //     var _this = this;
    //
    //     this.ms = this.$('#magicsuggest').magicSuggest({
    //         allowFreeEntries: false,
    //         groupBy: 'type',
    //         valueField: 'id',
    //         displayField: 'title',
    //         data: [],
    //         renderer: function(data){
    //             return '<div class="link-lato" data-civi-id="' + data.id +
    //             '"><span class="gray-text">'+data.type+'</span> ' + data.title + '</div>';
    //         },
    //         selectionRenderer: function(data){
    //             return '<span class="gray-text bold-text">'+data.type.toUpperCase() +'</span> '  + data.title;
    //         },
    //     });
    // },
    //
    // selectData: function() {
    //     var _this = this;
    //     var c_type = this.$el.find('.civi-types > .current').val();
    //     var linkableCivis = [];
    //     if (c_type == 'problem') {
    //         linkableCivis = _this.options.parentView.civis.where({type:'cause'});
    //     } else if (c_type == 'cause') {
    //         linkableCivis = _.union(_this.options.parentView.civis.where({type:'problem'}),
    //         _this.options.parentView.civis.where({type:'solution'}));
    //     } else if  (c_type == 'solution') {
    //         linkableCivis = _this.options.parentView.civis.where({type:'cause'});
    //     }
    //     var msdata = [];
    //     _.each(linkableCivis, function(c_model){
    //         var civi = {
    //             'id': c_model.get('id'),
    //             'type': c_model.get('type'),
    //             'title': c_model.get('title')
    //         };
    //         msdata.push(civi);
    //     });
    //     // console.log(msdata);
    //     this.ms.setData(msdata);
    // },

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

    createCivi: function (e) {
        var _this = this;

        var title = this.$el.find('#civi-title').val(),
            body = this.$el.find('#civi-body').val(),
            c_type = this.$el.find('.civi-types > .current').val();
        var links = this.magicSuggestView.ms.getValue();

        if (title && body && c_type) {
            $.ajax({
                url: '/api/new_civi/',
                type: 'POST',
                data: {
                    title: title,
                    body: body,
                    c_type: c_type,
                    thread_id: this.model.threadId,
                    links: links
                },
                success: function (response) {
                    _this.hide();
                    Materialize.toast('New civi created.', 2000);
                    var new_civi_data = response.data;
                    var new_civi = new cw.CiviModel(new_civi_data);
                    // TODO: change outline as well
                    var can_edit = new_civi.get('author').username == _this.options.parentView.username ? true : false;
                    $('#thread-' + c_type + 's').append(new cw.CiviView({model: new_civi, can_edit: can_edit, parentView: _this.options.parentView}).el);
                    _this.options.parentView.civis.add(new_civi);
                    _this.options.parentView.renderOutline(); //TODO: move renders into listeners
                    console.log(new_civi);
                    // _.each(new_civi.get('links'), function(link){
                    //     console.log(link);
                    //     _this.options.parentView.civis.findWhere({id: link}).view.render();
                    // });
                    _this.render();

                    $('body').css({overflow: 'hidden'});

                },
                error: function (response) {
                    Materialize.toast('Could not create Civi', 2000);
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

        var c_type = this.$el.find('.civi-types > .current').val();
        this.magicSuggestView.setLinkableData(c_type);
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
                    _this.options.parentView.responseCollection.fetch();
                    _this.options.parentView.renderResponses();
                    _this.render();

                }
            });
        } else {
            Materialize.toast('Please input all fields.', 2000);
        }
    }
});

cw.OutlineView = BB.View.extend({
});
cw.LinkSelectView = BB.View.extend({
    el: '#magicsuggest',

    initialize: function (options) {
        this.options = options || {};
        this.civis = options.civis;

        this.$el = options.$el || this.$el;
        this.setElement(this.$el);
        this.render();

        return this;
    },

    render: function(){
        var _this = this;

        this.ms = this.$el.magicSuggest({
            allowFreeEntries: false,
            groupBy: 'type',
            valueField: 'id',
            displayField: 'title',
            data: [],
            renderer: function(data){
                return '<div class="link-lato" data-civi-id="' + data.id +
                '"><span class="gray-text">'+data.type+'</span> ' + data.title + '</div>';
            },
            selectionRenderer: function(data){
                return '<span class="gray-text bold-text">'+data.type.toUpperCase() +'</span> '  + data.title;
            },
        });
    },

    setLinkableData: function(c_type) {
        var _this = this;
        var linkableCivis = [];
        if (c_type == 'problem') {
            linkableCivis = _this.civis.where({type:'cause'});
        } else if (c_type == 'cause') {
            linkableCivis = _.union(_this.civis.where({type:'problem'}),
            _this.civis.where({type:'solution'}));
        } else if  (c_type == 'solution') {
            linkableCivis = _this.civis.where({type:'cause'});
        }
        var msdata = [];
        _.each(linkableCivis, function(c_model){
            var civi = {
                'id': c_model.get('id'),
                'type': c_model.get('type'),
                'title': c_model.get('title')
            };
            msdata.push(civi);
        });
        // console.log(msdata);
        this.ms.setData(msdata);

        return this;
    },
});

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

        this.viewRecommended = true;
        this.initRecommended();

        this.responseCollection = new cw.ResponseCollection({}, {
            threadId: this.model.threadId
        });

        this.listenTo(this.responseCollection, 'sync', this.renderResponses);
    },

    initRecommended: function() {


        // 1. Get id list of voted civis\
        var votes = this.model.get('user_votes');
        //TODO: I dont like this
        // var problemIds = _.where(votes, {c_type: 'problem'}),
        //     causeIds = _.where(votes, {c_type: 'cause'}),
        //     solutionIds = _.where(votes, {c_type: 'solution'});

        // var recProblems = (_.indexOf(arrayIds, civi.id) > -1);
        // Mark each voted civi
        _.each(this.civis.models, function(civi){
            civi.recommended = false;
            civi.otherRecommended = false;
            var voteData = _.findWhere(votes, {civi_id: civi.id});
            if (!_.isUndefined(voteData)) {
                if ((voteData.activity_type == 'vote_pos' || voteData.activity_type == 'vote_vpos')){
                    _.each(civi.get('links'), function(link){
                        var linked_civi = this.civis.get(link);
                        if (!_.isUndefined(linked_civi) ) {
                            linked_civi.recommended = true;
                        }
                    }, this);
                } else {
                    _.each(civi.get('links'), function(link){
                        var linked_civi = this.civis.get(link);
                        if (!_.isUndefined(linked_civi) ) {
                            linked_civi.otherRecommended = true;
                        }
                    }, this);
                }
            }
        }, this);

        // _.each(this.civis.models, function(civi){
        //     if (civi.recommended) {
        //         _.each(civi.get('links'), function(link){
        //             var linked_civi = this.civis.get(link);
        //             if (!_.isUndefined(linked_civi) ) {
        //                 linked_civi.recommended = true;
        //                 console.log(linked_civi.id);
        //             }
        //         }, this);
        //     }
        // }, this);

        _.each(this.civis.filterByType('problem'), function(civi){
            civi.recommended = true;
            civi.otherRecommended = true;
        });
        // 2. Get id list of linked civis

        // 3. Populate collections based on recommended
        // this.problems = new cw.CiviSubCollection(this.civis.filterByType('problem'));
        // this.causes = new cw.CiviSubCollection(this.civis.filterByType('cause'));
        // this.solutions = new cw.CiviSubCollection(this.civis.filterByType('solution'));

        //
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
        this.$('.thread-body-holder').addClass('hide');

        this.threadWikiRender();
        this.threadBodyRender();
        this.$('.scroll-col').height($(window).height() - this.$('.body-banner').height());

        this.renderBodyContents();
    },

    threadWikiRender: function () {
        if (this.$('.thread-wiki-holder').length) {
            this.$('.thread-wiki-holder').empty().append(this.wikiTemplate());
        }
    },

    threadBodyRender: function () {
        var _this = this;

        if (this.$('.thread-body-holder').length) {
            this.$('.thread-body-holder').empty().append(this.bodyTemplate());

            this.$('.main-thread').on('scroll', function (e) {
                _this.processCiviScroll();
            });
        }
    },

    renderBodyContents: function () {
        this.renderCivis();
        this.renderOutline();
        this.renderVotes();
    },

    renderOutline: function(){
        // Render Outline Template based on models
        var problems = this.civis.filterByType('problem'),
            causes = this.civis.filterRecByType('cause', this.viewRecommended),
            solutions = this.civis.filterRecByType('solution', this.viewRecommended);

        var renderData = {
            problems: problems,
            causes: causes,
            solutions: solutions
        };

        var voteCount = { problem:0, cause:0, solution:0};
        var votes = this.model.get('user_votes'),
            voteIds = _.pluck(votes, 'civi_id');

        _.each(this.civis.filterByRec(this.viewRecommended), function(c){
            if (_.indexOf(voteIds, c.id) > -1) {
                voteCount[c.get('type')]++;
                // var votedCivi = this[v.c_type+'s'].get(v.civi_id);
                // if (!_.isUndefined(votedCivi)){
                //     this.voteCount
                // }
            }
        }, {this:this, voteCount:voteCount});

        var count = {
            problem: problems.length - voteCount.problem,
            cause: causes.length - voteCount.cause,
            solution: solutions.length - voteCount.solution,
            total: problems.length + causes.length + solutions.length,
        };

        count.total = count.problem + count.cause + count.solution;
        renderData.count = count;

        this.$('#civi-outline').empty().append(this.outlineTemplate(renderData));
        this.$('#recommended-switch').attr('checked', this.viewRecommended);

        if (this.viewRecommended){
            this.$(".label-recommended").addClass('current');
            this.$(".label-other").removeClass('current');
        } else {
            this.$(".label-recommended").removeClass('current');
            this.$(".label-other").addClass('current');
        }


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
        _.each(this.civis.filterByType('problem'), this.civiRenderHelper, this);
        _.each(this.civis.filterByType('cause'), this.civiRenderHelper, this);
        _.each(this.civis.filterByType('solution'), this.civiRenderHelper, this);
    },

    civiRenderHelper: function(civi){
        var can_edit = civi.get('author').username == this.username ? true : false;
        if (this.viewRecommended) {
            if (civi.recommended || civi.get('type') === 'problem') {
                this.$('#thread-'+civi.get('type')+'s').append(new cw.CiviView({model: civi, can_edit: can_edit, parentView: this}).el);
            }
        } else {
            if (civi.otherRecommended || civi.get('type') === 'problem') {
                this.$('#thread-'+civi.get('type')+'s').append(new cw.CiviView({model: civi, can_edit: can_edit, parentView: this}).el);
            }
        }

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
        this.$('.responses').empty().append(this.responseWrapper());
        _.each(this.responseCollection.models, function(civi){
            var can_edit = civi.get('author').username == this.username ? true : false;
            this.$('#response-list').append(new cw.CiviView({model: civi, can_edit: can_edit, parentView: this}).el);
        }, this);
    },

    events: {
        'click .enter-body': 'scrollToBody',
        'click .enter-wiki': 'scrollToWiki',
        'click .expand-nav': 'toggleExpandNav',
        'click .civi-nav-link': 'goToCivi',
        'click .civi-card': 'drilldownCivi',
        'click .add-civi': 'openNewCiviModal',
        'click .add-response': 'openNewResponseModal',
        'click #recommended-switch': 'toggleRecommended'
    },

    scrollToBody: function () {
        var _this = this;

        this.$('.thread-wiki-holder').addClass('hide');
        this.$('.thread-body-holder').removeClass('hide');
        this.$('.thread-body-holder').css({display: 'block'});

        $('body').css({overflow: 'hidden'});

        // this.$('.thread-body-holder').css({display: 'block'});
        // $('body').css({overflow: 'hidden'});
        //
        // $('body').animate({
        //     scrollTop: $('.thread-body-holder').offset().top
        // }, 200);

        var $civiNavScroll = this.$('.civi-outline');
        $civiNavScroll.css({height: $('body').height() - $civiNavScroll.offset().top});
        var $civiThreadScroll = this.$('.main-thread');
        $civiThreadScroll.css({height: $('body').height() - $civiThreadScroll.offset().top});
        var $civiResponseScroll = this.$('.responses');
        $civiResponseScroll.css({height: $('body').height() - $civiResponseScroll.offset().top});

        this.renderOutline();

        // this.currentScroll = 0;
        this.processCiviScroll();
    },


    scrollToWiki: function () {
        var _this = this;

        // $('body').animate({
        //     scrollTop: 0
        // }, 200, function () {
        //     _this.$('.thread-body-holder').css({display: 'none'});
        // });
        // $('body').css({overflow: 'scroll'});
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

        // if ($this.hasClass('expanded')) {
        //     $('.civi-nav-wrapper').slideUp();
        //     $this.removeClass('expanded');
        //     this.navExpanded = false;
        // } else {
        //     $('.civi-nav-wrapper').slideDown();
        //     $this.addClass('expanded');
        //     this.navExpanded = true;
        // }
        if (!this.navExpanded) {
            $('.civi-nav-wrapper').slideUp();
            $this.removeClass('expanded');
            // this.navExpanded = false;
        } else {
            $('.civi-nav-wrapper').slideDown();
            $this.addClass('expanded');
            // this.navExpanded = true;
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

    autoscrollCivi: _.throttle(function (target) {
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
            this.$('.responses').empty();
        }

    }, 250),

    drilldownCivi: function (e) {
        var $this = $(e.currentTarget);

        if ($this.find('.civi-type').text() != "response") {
            var $currentCivi = this.$('[data-civi-id="' + this.currentCivi + '"]'),
                $newCivi = $this.closest('.civi-card');

            if (this.currentCivi !== $newCivi.attr('data-civi-id')) {
                // $currentCivi.removeClass('current');
                this.$('.civi-card').removeClass('current');
                $newCivi.addClass('current');
                var civi_id = $newCivi.data('civi-id');

                var links = this.civis.get(civi_id).get('links');
                // var links_related = [];
                // _.each(links, function(link){
                //     links_related = this.$('#civi-'+link).data('civi-links');
                //     console.log(links_related);
                //     if (!links_related) return;
                //     if (links_related.length > 1){
                //         links_related= links_related.split(",").map(Number);
                //     } else {
                //         links_related = parseInt(links_related);
                //     }
                //
                //     links = _.union(links, links_related);
                // },this);
                // console.log(links);

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

                this.responseCollection.civiId = this.currentCivi;
                this.responseCollection.fetch();

            } else {
                $currentCivi.removeClass('current');
                this.$('.civi-card').removeClass('linked');

                this.currentCivi = null;
                this.$('.responses').empty();
            }
        }
    },

    toggleRecommended: function(e) {
        var target = $(e.currentTarget);
        var recommend_state = target.is(":checked");

        this.viewRecommended = recommend_state;

        this.$('.main-thread').scrollTop(0);
        this.renderBodyContents();
        this.processCiviScroll();
    },

    openNewCiviModal: function () {

        this.newCiviView.show();
    },

    openNewResponseModal: function () {
        this.newResponseView.show();
    },

    assign: function(view, selector) {
        view.setElement(this.$(selector)).render();
    }
});

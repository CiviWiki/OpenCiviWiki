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

    //     this.set({
    //        ratings: r,
    //        author: a,
    //        attachments: a
    //    });
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
            return civi.get("type").category_id === type;
        });
        return filtered;
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
    //
    // parse: function(data){
    //     var parsed_data= _.map(data, function(c){return JSON.parse(c);});
    //
    //     return parsed_data;
    // },

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
                    Materialize.toast('Could favor the civi', 2000);
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
                    Materialize.toast('Could favor the civi', 2000);
                }
            });
            $this.text('star_border');
        }
    },

    grabLink: function () {
        Materialize.toast('Civi link copied to clipboard.', 1500);
    },

    clickRating: function (e) {
        var _this = this;
        var $this = $(e.target).closest('.rating-button');

        var rating = $this.data('rating');
        var civi_id = $(e.target).closest('.civi-card').data('civi-id');

        if (this.can_edit) {
            Materialize.toast('Trying to vote on your own civi? :}', 2000);
            return;
        }
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
                    $this.addClass('current');
                    $this.siblings().removeClass('current');
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

        console.log(new_body, new_title);
        if (!new_body || !new_title){
            Materialize.toast('Please do not leave fields blank', 2000);
            return;
        } else if ((new_body == this.model.get('body') && new_title == this.model.get('title'))){
            this.closeEdit(e);
            return;
        } else {
            $.ajax({
                url: '/api/edit_civi/',
                type: 'POST',
                data: {
                    civi_id: this.model.id,
                    title: new_title,
                    body: new_body
                },
                success: function (response) {
                    Materialize.toast('Saved!', 2000);
                    // var score = $this.find('.rate-value');
                    // var new_vote = parseInt(score.text())+ 1;
                    // score.text(new_vote);
                    _this.model.set('title', new_title);
                    _this.model.set('body', new_body);
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
        this.renderMagicSuggest();
    },

    renderMagicSuggest: function() {
        var _this = this;

        this.ms = this.$('#magicsuggest').magicSuggest({
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

    selectData: function() {
        var _this = this;
        var c_type = this.$el.find('.civi-types > .current').val();
        var linkableCivis = [];
        if (c_type == 'problem') {
            linkableCivis = _this.options.parentView.civis.where({type:'cause'});
        } else if (c_type == 'cause') {
            linkableCivis = _.union(_this.options.parentView.civis.where({type:'problem'}),
            _this.options.parentView.civis.where({type:'solution'}));
        } else if  (c_type == 'solution') {
            linkableCivis = _this.options.parentView.civis.where({type:'cause'});
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
        var links = this.ms.getValue();

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

        this.selectData();
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

        this.responseCollection = new cw.ResponseCollection({}, {
            threadId: this.model.threadId
        });

        this.listenTo(this.responseCollection, 'sync', this.renderResponses);
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
        this.$('.civi-padding').height(this.$('.main-thread').height());
        this.renderCivis();
        this.renderVotes();

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

            this.renderOutline();
            this.$('.main-thread').on('scroll', function (e) {
                _this.changeNavScroll(e.target.scrollTop);
            });
        }
    },

    renderOutline: function(){
        this.$('#civi-outline').empty().append(this.outlineTemplate());
        this.calcCiviLocations();
    },

    renderCivis: function () {
        _.each(this.civis.where({type: "problem"}), function(civi){
            var can_edit = civi.get('author').username == this.username ? true : false;
            this.$('#thread-problems').append(new cw.CiviView({model: civi, can_edit: can_edit, parentView: this}).el);
        }, this);
        _.each(this.civis.where({type: "cause"}), function(civi){
            var can_edit = civi.get('author').username == this.username ? true : false;
            this.$('#thread-causes').append(new cw.CiviView({model: civi, can_edit: can_edit, parentView: this}).el);
        }, this);
        _.each(this.civis.where({type: "solution"}), function(civi){
            var can_edit = civi.get('author').username == this.username ? true : false;
            this.$('#thread-solutions').append(new cw.CiviView({model: civi, can_edit: can_edit, parentView: this}).el);
        }, this);
    },

    renderVotes: function() {
        var _this = this;
        var savedVotes = this.model.get('user_votes');
        console.log();
        _.each(savedVotes, function(v){
            this.$('#civi-'+ v.civi_id).find("." +v.activity_type).addClass('current');
        });
    },

    renderResponses: function () {
        this.$('.responses').empty().append(this.responseWrapper());
        _.each(this.responseCollection.models, function(civi){
            var can_edit = civi.get('author').username == this.username ? true : false;
            this.$('#response-list').append(new cw.CiviView({model: civi, can_edit: can_edit, parentView: this}).el);
        }, this);
    },

    changeNavScroll: function (scrollPosition, firstTime, navChange) {
        var _this = this;
        if (this.civis.length === 0){
            return;
        }
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

        var element = _.find(_this.civiLocations, function (l) {
            return scrollPosition > l.top - 16 && scrollPosition < l.bottom + 2;
        });

        if (!element) return;
        var newCivi = element.id;

        if (_this.currentNavCivi !== newCivi) {
            var $currentNavCivi = _this.$('[data-civi-nav-id="' + _this.currentNavCivi + '"]'),
                $newNavCivi = _this.$('[data-civi-nav-id="' + newCivi + '"]');

            $currentNavCivi.removeClass('current');
            $newNavCivi.addClass('current');

            _this.autoscrollCivi(_this.$('#civi-'+ newCivi));

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
        'click .add-civi': 'openNewCiviModal',
        'click .add-response': 'openNewResponseModal'
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

        this.calcCiviLocations();

        this.currentScroll = 0;

        _this.changeNavScroll(_this.currentScroll, true);
    },

    calcCiviLocations: function(){
        var _this = this;
        var threadPos = this.$('.main-thread').position().top;
        this.civiLocations = [];
        this.$('.civi-card').each(function (idx, civi) {
            var $civi = $(civi),
                $civiTop = $civi.position().top - threadPos;
            _this.civiLocations.push({top: $civiTop, bottom: $civiTop + $civi.height(), id: $civi.attr('data-civi-id')});
        });
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
        this.$('.main-thread').animate({scrollTop: _.findWhere(this.civiLocations, {id: $link.attr('data-civi-nav-id')}).top - 15}, 250);
    },
    autoscrollCivi: function (target) {
        var $this = target;

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

                _.each(this.$('.civi-card'), function(civiCard){
                    // console.log(links, $(civiCard).data('civi-id'));

                    if (links.indexOf($(civiCard).data('civi-id')) == -1 ){
                        $(civiCard).removeClass('linked');
                    } else {
                        $(civiCard).addClass('linked');
                    }
                });

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

                _.each(this.$('.civi-card'), function(civiCard){
                    // console.log(links, $(civiCard).data('civi-id'));

                    if (links.indexOf($(civiCard).data('civi-id')) == -1 ){
                        $(civiCard).removeClass('linked');
                    } else {
                        $(civiCard).addClass('linked');
                    }
                });

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

cw = cw || {};

cw.DEFAULTS = {
    types: ['problem', 'cause', 'solution'],
    types_plural: ['problems', 'causes', 'solutions'],
    civiViewStates: ['recommended', 'other'],
    viewLimit: 5,
};

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

// cw.CiviSubCollection = BB.Collection.extend({
//     model: cw.CiviModel,
//     comparator: function(model) {
//         return -model.get('score');
//     },
//
//     initialize: function (options) {
//         options = options || {};
//     },
// });

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
        'click .civi-image-thumb': 'viewImageModal',

        // 'click .civi-grab-link': 'grabLink',
        // vote
        // changevote

    },

    viewImageModal: function(e){
        var img_src = $(e.currentTarget).attr('src');
        var $modal = $('#civi-image-modal');
        $('#civi-image-big').attr('src', img_src);
        $modal.openModal();
        e.stopPropagation();
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
                    Materialize.toast('Favorited Civi', 5000);
                    $this.text('star');
                },
                error: function(r){
                    Materialize.toast('Could not favor the civi', 5000);
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
                    Materialize.toast('Favorited Civi', 5000);
                },
                error: function(r){
                    Materialize.toast('Could not favor the civi', 5000);
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
        //     Materialize.toast('Trying to vote on your own civi? :}', 5000);
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
                    Materialize.toast('Voted!', 5000);
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

                    if (_this.model.get('type') != "response") {
                        _this.parentView.initRecommended(); //THISTHIS
                        _this.parentView.renderBodyContents();
                        _this.parentView.processCiviScroll();
                    }

                    _this.$('.rating-button').removeClass('current');
                    $this.addClass('current');


                },
                error: function(r){
                    Materialize.toast('Could not vote :(', 5000);
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
            Materialize.toast('Please do not leave fields blank', 5000);
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
                    Materialize.toast('Saved!', 5000);
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
                    Materialize.toast('Could not edit the civi', 5000);
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
                Materialize.toast('Deleted Civi succssfully', 5000);
                _.each(_this.model.links, function(link){
                    _this.civis.findWhere({id: link}).view.render();
                });

                _this.civis.remove(_this.model);
                _this.remove();
                _this.parentView.initRecommended();
                _this.parentView.renderBodyContents();

            },
            error: function(r){
                Materialize.toast('Could not delete the civi', 5000);
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

    show: function () {
        this.$('.new-civi-modal').openModal();
    },

    hide: function () {
        this.$('.new-civi-modal').closeModal();
    },

    events: {
        'click .cancel-new-civi': 'cancelCivi',
        'click .create-new-civi': 'createCivi',
        'click .civi-type-button': 'clickType',
        'change .attachment-image-pick': 'previewImageNames'
    },


    previewImageNames: function(e) {
        var attachment_input = this.$el.find('#id_attachment_image');
        var uploaded_images = attachment_input[0].files;
        console.log(attachment_input);
        this.$('.file-preview').empty().append("<div>"+uploaded_images.length+" Images</div>");
        _.each(uploaded_images, function(img_file){
            console.log(img_file);
            this.$('.file-preview').append("<div class=\"link-lato gray-text\">"+img_file.name+"</div>");
        }, this);

        this.attachmentCount = uploaded_images.length;

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

        this.$(e.currentTarget).addClass('disabled').attr('disabled', true);

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
                    var attachment_input = _this.$('#id_attachment_image');
                    var uploaded_images = attachment_input[0].files;
                    if (uploaded_images.length > 0) {
                        var formData = new FormData(_this.$('#attachment_image_form')[0]);
                        formData.set('civi_id', response.data.id);
                        $.ajax({
                            url: '/api/upload_images/',
                            type: 'POST',
                            success: function (response2) {
                                _this.hide();
                                Materialize.toast('New civi created.', 5000);
                                var new_civi_data = response.data;
                                var new_civi = new cw.CiviModel(new_civi_data);
                                new_civi.set('attachments', response2.attachments);
                                // TODO: change outline as well
                                var can_edit = new_civi.get('author').username == _this.options.parentView.username ? true : false;
                                $('#thread-' + c_type + 's').append(new cw.CiviView({model: new_civi, can_edit: can_edit, parentView: _this.options.parentView}).el);
                                _this.options.parentView.civis.add(new_civi);

                                // if(c_type ==='problem'){
                                //     this.recommendedCivis.push(new_civi.id);
                                //     this.otherCivis.push(new_civi.id);
                                // }
                                _this.options.parentView.initRecommended();
                                _this.options.parentView.renderBodyContents(); //TODO: move renders into listeners
                                // _.each(new_civi.get('links'), function(link){
                                //     console.log(link);
                                //     _this.options.parentView.civis.findWhere({id: link}).view.render();
                                // });
                                _this.render();

                                $('body').css({overflow: 'hidden'});
                            },
                            error: function(e){
                                Materialize.toast('ERROR: Image could not be uploaded', 5000);
                                Materialize.toast(e.statusText, 5000);
                                _this.$(e.currentTarget).removeClass('disabled').attr('disabled', false);
                            },
                            data: formData,
                            cache: false,
                            contentType: false,
                            processData: false
                        });
                    } else {
                        _this.hide();
                        Materialize.toast('New civi created.', 5000);
                        var new_civi_data = response.data;
                        var new_civi = new cw.CiviModel(new_civi_data);
                        var can_edit = new_civi.get('author').username == _this.options.parentView.username ? true : false;
                        $('#thread-' + c_type + 's').append(new cw.CiviView({model: new_civi, can_edit: can_edit, parentView: _this.options.parentView}).el);
                        _this.options.parentView.civis.add(new_civi);

                        var parent_links = new_civi.get('links');
                        _.each(parent_links, function(parent_id){
                            var parent_civi = _this.options.parentView.civis.get(parent_id)
                            if (parent_civi) {
                                var prev_links = parent_civi.get('links');
                                prev_links.push(new_civi.id);
                                parent_civi.set('links', prev_links);
                            }

                        }, this);
                        // if(c_type ==='problem'){
                        //     this.recommendedCivis.push(new_civi.id);
                        //     this.otherCivis.push(new_civi.id);
                        // }
                        _this.options.parentView.initRecommended();
                        _this.options.parentView.renderBodyContents(); //TODO: move renders into listeners
                        // _.each(new_civi.get('links'), function(link){
                        //     console.log(link);
                        //     _this.options.parentView.civis.findWhere({id: link}).view.render();
                        // });
                        _this.render();
                    }



                },
                error: function (response) {
                    Materialize.toast('Could not create Civi', 5000);
                    _this.$(e.currentTarget).removeClass('disabled').attr('disabled', false);
                }
            });
        } else {
            Materialize.toast('Please input all fields.', 5000);
            this.$(e.currentTarget).removeClass('disabled').attr('disabled', false);
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
        'change .attachment-image-pick': 'previewImageNames'
    },

    show: function () {
        this.$('.new-response-modal').openModal();
    },

    previewImageNames: function(e) {
        var attachment_input = this.$el.find('#response_attachment_image');
        var uploaded_images = attachment_input[0].files;
        console.log(attachment_input);
        this.$('.file-preview').empty().append("<div>"+uploaded_images.length+" Images</div>");
        _.each(uploaded_images, function(img_file){
            console.log(img_file);
            this.$('.file-preview').append("<div class=\"link-lato gray-text\">"+img_file.name+"</div>");
        }, this);

        this.attachmentCount = uploaded_images.length;

    },

    createResponse: function (e) {
        var _this = this;
        this.$(e.currentTarget).addClass('disabled').attr('disabled', true);
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
                    var attachment_input = _this.$('#response_attachment_image');
                    var uploaded_images = attachment_input[0].files;
                    if (uploaded_images.length > 0) {
                        var formData = new FormData(_this.$('#response_attachment_image_form')[0]);
                        formData.set('civi_id', response.data.id);
                        $.ajax({
                            url: '/api/upload_images/',
                            type: 'POST',
                            success: function (response2) {
                                Materialize.toast('New response created.', 5000);
                                _this.options.parentView.responseCollection.fetch();
                                _this.options.parentView.renderResponses();
                                _this.render();
                            },
                            error: function(e){
                                Materialize.toast('Could not create response', 5000);
                                _this.$(e.currentTarget).removeClass('disabled').attr('disabled', false);
                            },
                            data: formData,
                            cache: false,
                            contentType: false,
                            processData: false
                        });
                    } else {
                        Materialize.toast('New response created.', 5000);
                        _this.options.parentView.responseCollection.fetch();
                        _this.options.parentView.renderResponses();
                        _this.render();
                    }
                },
                error: function(){
                    Materialize.toast('Could not create response', 5000);
                    _this.$(e.currentTarget).removeClass('disabled').attr('disabled', false);
                }
            });
        } else {
            Materialize.toast('Please input all fields.', 5000);
            _this.$(e.currentTarget).removeClass('disabled').attr('disabled', false);
        }
    }
});

cw.EditThreadView = BB.View.extend({
    el: '.edit-thread-modal-holder',
    template: _.template($('#edit-thread-template').html()),
    initialize: function (options) {
        this.options = options || {};
        this.threadId = options.threadId;
        this.parentView = options.parentView;
        this.removeImage = false;
        this.render();
    },

    render: function () {
        this.$el.empty().append(this.template());
        this.$('#attachment_image_form').addClass('hide');
        cw.materializeShit();
    },

    events: {
        'click .create-new-response': 'createResponse',
        'click .cancel-thread': 'cancelEdit',
        'click .delete-previous-image': 'showImageForm',
        'click .use-previous-image': 'hideImageForm',
        'click .edit-thread': 'editThread'
    },

    show: function () {
        this.$('.edit-thread-modal').openModal();
    },

    hide: function () {
        this.$('.edit-thread-modal').closeModal();
    },

    cancelEdit: function () {
        this.hide();
        this.render();
    },

    showImageForm: function () {
        this.$('#attachment_image_form').removeClass('hide');
        this.$('.previous-image').addClass('hide');
        this.removeImage = true;
    },

    hideImageForm: function () {
        this.$('#attachment_image_form').addClass('hide');
        this.$('.previous-image').removeClass('hide');
        this.removeImage = false;
    },

    editThread: function (e) {
        var _this = this;
        _this.$(e.currentTarget).addClass('disabled').attr('disabled', true);

        var title = this.$el.find('#thread-title').val().trim(),
            summary = this.$el.find('#thread-body').val().trim(),
            category_id = this.$el.find('#thread-category').val();

        var thread_id = this.threadId;
        console.log(title, summary, category_id, thread_id);
        if (title && summary && category_id) {
            $.ajax({
                url: '/api/edit_thread/',
                type: 'POST',
                data: {
                    title: title,
                    summary: summary,
                    category_id: category_id,
                    thread_id: thread_id
                },
                success: function (response) {
                    var file = $('#thread_attachment_image').val();

                    if (_this.removeImage && file) {
                        var formData = new FormData(_this.$('#attachment_image_form')[0]);
                        formData.set('thread_id', response.data.thread_id);
                        $.ajax({
                            url: '/api/upload_image/',
                            type: 'POST',
                            success: function (response2) {
                                Materialize.toast('Saved changes', 5000);
                                _this.hide();


                                new_data = response.data;
                                _this.parentView.model.set('title', new_data.title);
                                _this.parentView.model.set('summary', new_data.summary);
                                _this.parentView.model.set('category', new_data.category);
                                _this.parentView.model.set('image', response2.image);
                                _this.parentView.threadWikiRender();
                                _this.render();  // TODO: Please remove this
                            },
                            error: function(e){
                                Materialize.toast('ERROR: Image could not be uploaded', 5000);
                                Materialize.toast(e.statusText, 5000);
                            },
                            data: formData,
                            cache: false,
                            contentType: false,
                            processData: false
                        });
                    } else {
                        Materialize.toast('Saved changes', 5000);
                        _this.hide();

                        // New Data
                        new_data = response.data;
                        _this.parentView.model.set('title', new_data.title);
                        _this.parentView.model.set('summary', new_data.summary);
                        _this.parentView.model.set('category',new_data.category);
                        _this.parentView.threadWikiRender();
                        _this.render(); // TODO: Please remove this
                    }

                },
                error: function() {
                    Materialize.toast('Servor Error: Thread could not be edited', 5000);
                    _this.$(e.currentTarget).removeClass('disabled').attr('disabled', false);
                }
            });
        } else {
            Materialize.toast('Please input all fields.', 5000);
            _this.$(e.currentTarget).removeClass('disabled').attr('disabled', false);
        }
    },
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
        //TODO: I dont like this
        // var problemIds = _.where(votes, {c_type: 'problem'}),
        //     causeIds = _.where(votes, {c_type: 'cause'}),
        //     solutionIds = _.where(votes, {c_type: 'solution'});

        // var recProblems = (_.indexOf(arrayIds, civi.id) > -1);
        // Mark each voted civi
        // _.each(this.civis.models, function(civi){
        //     civi.recommended = false;
        //     civi.otherRecommended = false;
        //     var voteData = _.findWhere(votes, {civi_id: civi.id});
        //     if (!_.isUndefined(voteData)) {
        //         if ((voteData.activity_type == 'vote_pos' || voteData.activity_type == 'vote_vpos')){
        //             _.each(civi.get('links'), function(link){
        //                 var linked_civi = this.civis.get(link);
        //                 if (!_.isUndefined(linked_civi) ) {
        //                     linked_civi.recommended = true;
        //                 }
        //             }, this);
        //         } else {
        //             _.each(civi.get('links'), function(link){
        //                 var linked_civi = this.civis.get(link);
        //                 if (!_.isUndefined(linked_civi) ) {
        //                     linked_civi.otherRecommended = true;
        //                 }
        //             }, this);
        //         }
        //     }
        // }, this);

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
                        if (!_.isUndefined(linked_civi) ) {
                            this.recommendedCivis.push(link);
                            // linked_civi.recommended = true;
                        }
                    }, this);
                } else {
                    _.each(civi.get('links'), function(link){
                        var linked_civi = this.civis.get(link);
                        if (!_.isUndefined(linked_civi) ) {
                            this.otherCivis.push(link);

                        }
                    }, this);
                }
            } else {
                civi.voted = false;
            }
        }, this);

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

        // _.each(this.civis.filterByType('problem'), function(civi){
        //     civi.recommended = true;
        //     civi.otherRecommended = true;
        // });
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

        this.editThreadView = new cw.EditThreadView({
            model: this.model,
            parentView: this,
            threadId: this.model.threadId
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
        var _this = this;
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

        var count = {
            problem: highlightCount.problem - recCount.problem,
            cause: highlightCount.cause - voteCount.cause,
            solution: highlightCount.solution - voteCount.solution,
        };

        count.totalRec = this.civiRecViewTotals.problem + this.civiRecViewTotals.cause + this.civiRecViewTotals.solution - recCount.problem - recCount.cause - recCount.solution;
        count.totalOther = this.civiOtherViewTotals.problem + this.civiOtherViewTotals.cause + this.civiOtherViewTotals.solution - recCount.problem - otherCount.cause - otherCount.solution;

        renderData.count = count;

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

            if(totalCount > limit) {
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
        var can_edit = civi.get('author').username == this.username ? true : false;
        this.$('#thread-'+civi.get('type')+'s').append(new cw.CiviView({model: civi, can_edit: can_edit, parentView: this}).el);

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

            var vote = _.find(this.model.get('user_votes'), function(v){
                return v.civi_id === civi.id;
            });
            if (vote) {
                this.$('#civi-'+ vote.civi_id).find("." +vote.activity_type).addClass('current');
            }
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
        'click #recommended-switch': 'toggleRecommended',
        'click .btn-loadmore': 'loadMoreCivis',
        'click .edit-thread-button': 'openEditThreadModal'
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
            $('.civi-nav-wrapper').hide();
            $this.removeClass('expanded');
            // this.navExpanded = false;
        } else {
            $('.civi-nav-wrapper').show();
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
            this.$('.responses').empty();
        }

    },

    drilldownCivi: function (e) {
        if ($(e.target).hasClass('rating-button')) {
            return;
        }
        var $this = $(e.currentTarget);
        if ($this.find('.civi-type').text() != "response") {
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
                this.$('.responses').empty();
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

    openNewCiviModal: function () {

        this.newCiviView.show();
    },

    openNewResponseModal: function () {
        this.newResponseView.show();
    },

    openEditThreadModal: function() {
        this.editThreadView.show();
    },

    assign: function(view, selector) {
        view.setElement(this.$(selector)).render();
    }
});

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
        this.is_draft = options.is_draft;
        this.can_respond = options.can_respond;
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
        'click .edit': 'clickEdit',
        'click .delete': 'deleteEdit',
        'click .edit-confirm': 'saveEdit',
        'click .edit-cancel': 'closeEdit',
        'click .civi-image-thumb': 'viewImageModal',
        'change #civi-type-form': 'clickNewType',
        'click .delete-civi-image': 'addImageToDeleteList',
        'click #add-more-images': 'showImageForm',
        'change .attachment-image-pick': 'previewImageNames',
        'input .civi-link-images': 'previewImageNames',
        'click #add-image-link-input': 'addImageLinkInput',
        'click #respond-button': 'addRebuttal',
    },

    addImageLinkInput: function(){
        var link_images = this.$('.civi-link-images').length;
        if (link_images > 20 ) {
            Materialize.toast("Don't think you need any more...", 5000);
        } else {
            this.$('.image-link-list').append('<input type="text" class="civi-link-images" placeholder="Paste your image link here..."/>');
        }

    },

    previewImageNames: function(e) {
        var attachment_input = this.$('#id_attachment_image');
        var uploaded_images = attachment_input[0].files;
        var $previewlist = this.$('.file-preview');
        $previewlist.empty();
        // File Upload Images
        _.each(uploaded_images, function(img_file){
            $previewlist.append("<div class=\"link-lato gray-text preview-item \">"+img_file.name+"</div>");
        }, this);

        // Link Images
        this.attachment_links = [];
        var link_images = $('.civi-link-images');
        _.each(link_images, function(img_link){
            var link_value = img_link.value.trim();
            if (link_value){
                $previewlist.append("<div class=\"link-lato gray-text preview-item \">"+link_value+"</div>");
                this.attachment_links.push(link_value);
            }
        }, this);

        // Total images count
        var image_total = uploaded_images.length + this.attachment_links.length;
        if (image_total === 0) {
            $previewlist.prepend("<div>No Images</div>");
        } else if (image_total === 1) {
            $previewlist.prepend("<div>1 Image</div>");
        } else {
            $previewlist.prepend("<div>" + image_total + " Images</div>");
        }

        this.attachmentCount = image_total;

    },

    showImageForm: function(e){
        // HEREHERE
        this.$('.edit-images').removeClass('hide');
        this.$('#add-more-images').addClass('hide');
    },

    viewImageModal: function(e){
        var img_src = $(e.currentTarget).attr('src');
        var $modal = $('#civi-image-modal');
        $('#civi-image-big').attr('src', img_src);
        $modal.openModal();
        e.stopPropagation();
    },
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

                    if (_this.model.get('type') != "response" && _this.model.get('type') != "rebuttal") {
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
        // Populate with data TODO: move to a template
        this.$('.edit-civi-body').text(this.model.get('body'));
        this.$('.edit-civi-title').val(this.model.get('title'));
        this.$('#'+ this.model.get('type') + "-" + this.model.id).prop("checked", true);
        if (this.model.get('type') != 'response' && this.model.get('type') != 'rebuttal') {
            this.magicSuggestView = new cw.LinkSelectView({$el: this.$('#magicsuggest-'+this.model.id), civis: this.civis});
            this.magicSuggestView.setLinkableData(this.model.get('type'));
            this.magicSuggestView.ms.setValue(this.model.get('links'));
        }
        this.attachment_links = [];
        this.attachmentCount = 0;

        this.imageRemoveList = [];

        this.$('.edit-wrapper').removeClass('hide');
        this.$('.edit-action').removeClass('hide');
        this.$('.text-wrapper').addClass('hide');
        this.$('.edit').addClass('hide');
        this.$('.delete').addClass('hide');

        if (this.model.get('type') === 'response' || this.model.get('type') === 'rebuttal') {
            this.$('.edit-links').addClass('hide');
            this.$('#civi-type-form').addClass('hide');
        } else if (this.model.get('type') === 'problem') {
            this.$('#magicsuggest-'+this.model.id).addClass('hide');
        }
    },

    clickNewType: function(e){
        var new_type = $(e.target).closest("input[type='radio']:checked").val();
        // var new_type = $("#civi-type-form input[type='radio']:checked").val();
        if (new_type === "problem") {
            this.$('.edit-links').addClass('hide');
            this.$('#magicsuggest-'+this.model.id).addClass('hide');
        } else {
            this.$('.edit-links').removeClass('hide');
            this.$('#magicsuggest-'+this.model.id).removeClass('hide');
        }
        this.magicSuggestView.setLinkableData(new_type);
        this.magicSuggestView.ms.clear();
    },

    addRebuttal: function(){
        this.parentView.newResponseView.rebuttal_ref = this.model.id;
        this.parentView.newResponseView.render();
        this.parentView.newResponseView.show();
    },


    addImageToDeleteList: function(e) {
        var target = $(e.currentTarget);
        var target_image = target.data('image-id');

        this.imageRemoveList.push(target_image);
        target.remove();
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
        var c_type = this.model.get('type');
        var new_body = this.$('.edit-civi-body').val().trim();
            new_title = this.$('.edit-civi-title').val().trim();
        var links;
        if (c_type != 'response' && c_type != 'rebuttal') {
            links= this.magicSuggestView.ms.getValue();
        } else {
            links = [];
        }

        var new_type = this.$("#civi-type-form input[type='radio']:checked").val();

        if (!new_body || !new_title){
            Materialize.toast('Please do not leave fields blank', 5000);
            return;
        } else if (this.imageRemoveList.length===0 && this.attachmentCount===0 && (new_body == this.model.get('body') && new_title == this.model.get('title') && _.isEqual(links, this.model.get('links')) && new_type == this.model.get('type') )){
            this.closeEdit(e);
            return;
        } else {
            var data;


            if (c_type === 'response' || c_type === 'rebuttal') {
                new_type = c_type;
                data = {
                    civi_id: this.model.id,
                    title: new_title,
                    body: new_body
                };
            } else {
                data = {
                    civi_id: this.model.id,
                    title: new_title,
                    body: new_body,
                    links: links,
                    type: new_type
                };
            }

            if (this.imageRemoveList.length){
                data.image_remove_list = this.imageRemoveList;
            }

            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });

            $.ajax({
                url: '/api/edit_civi/',
                type: 'POST',
                data: data,
                success: function (response) {
                    _this.closeEdit(e);
                    // var score = $this.find('.rate-value');
                    // var new_vote = parseInt(score.text())+ 1;
                    // score.text(new_vote);
                    //
                    var attachment_input = _this.$('#id_attachment_image');
                    var uploaded_images = attachment_input[0].files;
                    if (_this.attachmentCount > 0) {
                        var formData = new FormData(_this.$('#attachment_image_form')[0]);
                        formData.set('civi_id', _this.model.id);
                        if (_this.attachment_links.length){
                            _.each(_this.attachment_links, function(img_link){
                                formData.append('attachment_links[]', img_link);
                            });
                        }

                        $.ajaxSetup({
                            beforeSend: function(xhr, settings) {
                                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                                }
                            }
                        });

                        $.ajax({
                            url: '/api/upload_images/',
                            type: 'POST',
                            success: function (response2) {

                                Materialize.toast('Saved.', 5000);

                                // Set the models with new data and rerender
                                _this.model.set('title', new_title);
                                _this.model.set('body', new_body);
                                _this.model.set('links', links);
                                _this.model.set('type', new_type);
                                _this.model.set('attachments', response2.attachments);
                                _this.model.set('score', response.score);
                                if (_this.magicSuggestView){
                                    _this.magicSuggestView.remove();
                                }

                                _this.render();

                                if (_this.model.get('type') != "response" && _this.model.get('type') != "rebuttal") {
                                    var parent_links = _this.model.get('links');
                                    _.each(parent_links, function(parent_id){
                                        var parent_civi = _this.options.parentView.civis.get(parent_id);
                                        if (parent_civi) {
                                            var prev_links = parent_civi.get('links');
                                            prev_links.push(_this.model.id);
                                            parent_civi.set('links', prev_links);
                                        }

                                    }, this);

                                    _this.parentView.initRecommended(); //THISTHIS
                                    _this.parentView.renderBodyContents();
                                    _this.parentView.processCiviScroll();
                                }
                            },
                            error: function(e){
                                Materialize.toast('Civi was edited but one or more images could not be uploaded', 5000);

                                // Set the models with new data and rerender
                                _this.model.set('title', new_title);
                                _this.model.set('body', new_body);
                                _this.model.set('links', links);
                                _this.model.set('type', new_type);
                                _this.model.set('attachments', response2.attachments);
                                _this.model.set('score', response.score);
                                if (_this.magicSuggestView){
                                    _this.magicSuggestView.remove();
                                }

                                _this.render();

                                if (_this.model.get('type') != "response" && _this.model.get('type') != "rebuttal") {
                                    var parent_links = _this.model.get('links');
                                    _.each(parent_links, function(parent_id){
                                        var parent_civi = _this.options.parentView.civis.get(parent_id);
                                        if (parent_civi) {
                                            var prev_links = parent_civi.get('links');
                                            prev_links.push(_this.model.id);
                                            parent_civi.set('links', prev_links);
                                        }

                                    }, this);

                                    _this.parentView.initRecommended(); //THISTHIS
                                    _this.parentView.renderBodyContents();
                                    _this.parentView.processCiviScroll();
                                }
                            },
                            data: formData,
                            cache: false,
                            contentType: false,
                            processData: false
                        });

                    } else {
                        Materialize.toast('Saved', 5000);

                        // Clean up previous links
                        if (_this.model.get('type') != "response" && _this.model.get('type') != "rebuttal") {
                            var orig_links = _this.model.get('links');
                            _.each(orig_links, function(parent_id){
                                var parent_civi = _this.options.parentView.civis.get(parent_id);
                                if (parent_civi) {
                                    var prev_links = parent_civi.get('links');
                                    var cleaned = _.without(prev_links, _this.model.id);
                                    parent_civi.set('links', cleaned);
                                }
                            }, this);
                        }
                        // Set the models with new data and rerender
                        _this.model.set('title', new_title);
                        _this.model.set('body', new_body);
                        _this.model.set('links', links);
                        _this.model.set('type', new_type);
                        _this.model.set('attachments', response.attachments);
                        _this.model.set('score', response.score);
                        if (_this.magicSuggestView){
                            _this.magicSuggestView.remove();
                        }

                        _this.render();

                        if (_this.model.get('type') != "response" && _this.model.get('type') != "rebuttal") {
                            var parent_links = _this.model.get('links');
                            _.each(parent_links, function(parent_id){
                                var parent_civi = _this.options.parentView.civis.get(parent_id);
                                if (parent_civi) {
                                    var prev_links = parent_civi.get('links');
                                    prev_links.push(_this.model.id);
                                    parent_civi.set('links', prev_links);
                                }
                            }, this);

                            _this.parentView.initRecommended(); //THISTHIS
                            _this.parentView.renderBodyContents();
                            _this.parentView.processCiviScroll();
                        }
                    }


                },
                error: function(r){
                    Materialize.toast('Could not edit the civi', 5000);
                    _this.closeEdit(e);
                    _this.render();

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
                csrfmiddlewaretoken: csrftoken,
                civi_id: this.model.id,
            },
            success: function (response) {
                Materialize.toast('Deleted Civi succssfully', 5000);
                _.each(_this.model.get('links'), function(link){
                    var linked_civi = _this.civis.findWhere({id: link});
                    var prev_links =linked_civi.get('links');
                    new_links = _.without(prev_links, _this.model.id);
                    linked_civi.set('links', new_links);
                });

                _this.civis.remove(_this.model);
                _this.remove();
                _this.parentView.initRecommended();
                _this.parentView.renderBodyContents();
                _this.parentView.processCiviScroll();

            },
            error: function(r){
                Materialize.toast('Could not delete the civi', 5000);
            }
        });
    }
});

cw.NewCiviView = BB.View.extend({
    el: '#new-civi-box',
    template: _.template($('#new-civi-template').html()),

    initialize: function (options) {
        this.options = options || {};
    },

    render: function () {
        this.$el.empty().append(this.template());
        // $('.responses').height($('#new-civi-box').height() + $('.responses-box').height());

        this.magicSuggestView = new cw.LinkSelectView(
            {$el: this.$('#magicsuggest'), civis: this.options.parentView.civis}
        );

        this.$('.edit-links').addClass('hide');
        this.$('#magicsuggest').addClass('hide');

        this.attachment_links = [];
        this.attachmentCount = 0;
        // this.renderMagicSuggest();
    },

    events: {
        'click .cancel-new-civi': 'cancelCivi',
        'click .create-new-civi': 'createCivi',
        'click .civi-type-button': 'clickType',
        'change .attachment-image-pick': 'previewImageNames',
        'input .civi-link-images': 'previewImageNames',
        'click #image-from-computer': 'showImageUploadForm',
        'click #image-from-link': 'showImageLinkForm',
        'click #add-image-link-input': 'addImageLinkInput',
        'click .ms-sel-ctn': ''
    },

    addImageLinkInput: function(){
        var link_images = this.$('.civi-link-images').length;
        if (link_images > 20 ) {
            Materialize.toast("Don't think you need any more...", 5000);
        } else {
            this.$('.image-link-list').append('<input type="text" class="civi-link-images" placeholder="Paste your image link here..."/>');
        }

    },

    previewImageNames: function(e) {
        var attachment_input = this.$('#id_attachment_image');
        var uploaded_images = attachment_input[0].files;
        var $previewlist = this.$('.file-preview');
        $previewlist.empty();
        // File Upload Images
        _.each(uploaded_images, function(img_file){
            $previewlist.append("<div class=\"link-lato gray-text preview-item \">"+img_file.name+"</div>");
        }, this);

        // Link Images
        this.attachment_links = [];
        var link_images = $('.civi-link-images');
        _.each(link_images, function(img_link){
            var link_value = img_link.value.trim();
            if (link_value){
                $previewlist.append("<div class=\"link-lato gray-text preview-item \">"+link_value+"</div>");
                this.attachment_links.push(link_value);
            }
        }, this);

        // Total images count
        var image_total = uploaded_images.length + this.attachment_links.length;
        if (image_total === 0) {
            $previewlist.prepend("<div>No Images</div>");
        } else if (image_total === 1) {
            $previewlist.prepend("<div>1 Image</div>");
        } else {
            $previewlist.prepend("<div>" + image_total + " Images</div>");
        }

        this.attachmentCount = image_total;

    },

    cancelCivi: function () {
        this.$el.empty();
    },

    createCivi: function (e) {
        var _this = this;

        var title = this.$el.find('#civi-title').val(),
            body = this.$el.find('#civi-body').val(),
            c_type = this.$el.find('.civi-types > .current').val();
        var links = this.magicSuggestView.ms.getValue();

        this.$(e.currentTarget).addClass('disabled').attr('disabled', true);

        if (title && body && c_type) {
            if (links.length === 0) {
                if (c_type === 'cause') {
                    Materialize.toast('A CAUSE Civi must be linked to a PROBLEM Civi. If it is only linked to a solution it will not appear', 5000);
                    this.$(e.currentTarget).removeClass('disabled').attr('disabled', false);
                    return;
                } else if (c_type === 'solution') {
                    Materialize.toast('A SOLUTION Civi must be linked to a CAUSE Civi', 5000);
                    this.$(e.currentTarget).removeClass('disabled').attr('disabled', false);
                    return;
                }
            }
            $.ajax({
                url: '/api/new_civi/',
                type: 'POST',
                data: {
                    csrfmiddlewaretoken: csrftoken,
                    title: title,
                    body: body,
                    c_type: c_type,
                    thread_id: _this.model.threadId,
                    links: links,
                },
                success: function (response) {
                    var new_civi_data = response.data;
                    var new_civi = new cw.CiviModel(new_civi_data);
                    var can_edit = new_civi.get('author').username == _this.options.parentView.username ? true : false;

                    var attachment_input = _this.$('#id_attachment_image');
                    var uploaded_images = attachment_input[0].files;
                    if (_this.attachmentCount > 0) {
                        var formData = new FormData(_this.$('#attachment_image_form')[0]);
                        formData.set('civi_id', response.data.id);
                        if (_this.attachment_links.length){
                            _.each(_this.attachment_links, function(img_link){
                                formData.append('attachment_links[]', img_link);
                            });
                        }

                        $.ajaxSetup({
                            beforeSend: function(xhr, settings) {
                                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                                }
                            }
                        });

                        $.ajax({
                            url: '/api/upload_images/',
                            type: 'POST',
                            success: function (response2) {

                                Materialize.toast('New civi created.', 5000);
                                new_civi.set('attachments', response2.attachments);

                                // _this.hide();
                                $('#thread-' + c_type + 's').append(new cw.CiviView({model: new_civi, can_edit: can_edit, parentView: _this.options.parentView}).el);
                                _this.options.parentView.civis.add(new_civi);

                                _this.options.parentView.initRecommended();
                                _this.options.parentView.renderBodyContents(); //TODO: move renders into listeners

                                _this.$el.empty();

                                $('body').css({overflow: 'hidden'});
                            },
                            error: function(e){
                                Materialize.toast('Civi was created but one or more images could not be uploaded', 5000);

                                // _this.hide();
                                $('#thread-' + c_type + 's').append(new cw.CiviView({model: new_civi, can_edit: can_edit, parentView: _this.options.parentView}).el);
                                _this.options.parentView.civis.add(new_civi);

                                _this.options.parentView.initRecommended();
                                _this.options.parentView.renderBodyContents(); //TODO: move renders into listeners

                                _this.$el.empty();

                                $('body').css({overflow: 'hidden'});
                            },
                            data: formData,
                            cache: false,
                            contentType: false,
                            processData: false
                        });

                    } else {
                        // _this.hide();
                        Materialize.toast('New civi created.', 5000);
                        $('#thread-' + c_type + 's').append(new cw.CiviView({model: new_civi, can_edit: can_edit, parentView: _this.options.parentView}).el);
                        _this.options.parentView.civis.add(new_civi);

                        var parent_links = new_civi.get('links');
                        _.each(parent_links, function(parent_id){
                            var parent_civi = _this.options.parentView.civis.get(parent_id);
                            if (parent_civi) {
                                var prev_links = parent_civi.get('links');
                                prev_links.push(new_civi.id);
                                parent_civi.set('links', prev_links);
                            }

                        }, this);

                        _this.options.parentView.initRecommended();
                        _this.options.parentView.renderBodyContents(); //TODO: move renders into listeners

                        _this.$el.empty();
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

        if (c_type === "problem") {
            this.$('.edit-links').addClass('hide');
            this.$('#magicsuggest').addClass('hide');
        } else {
            this.$('.edit-links').removeClass('hide');
            this.$('#magicsuggest').removeClass('hide');
            this.magicSuggestView.setLinkableData(c_type);
            this.magicSuggestView.ms.clear();
        }

    },
});

cw.NewResponseView = BB.View.extend({
    el: '#new-response-box',
    template: _.template($('#new-response-template').html()),
    initialize: function (options) {
        this.options = options || {};
        this.rebuttal_ref = '';
    },

    render: function () {
        this.$el.empty().append(this.template());
        $('#add-new-response').hide();

        this.attachment_links = [];
        this.attachmentCount = 0;
    },

    events: {
        'click .create-new-response': 'createResponse',
        'change .attachment-image-pick': 'previewImageNames',
        'click .cancel-new-response': 'hide',
        'input .civi-link-images': 'previewImageNames',
        'click #add-image-link-input': 'addImageLinkInput',
    },
    hide: function () {
        $('#new-response-box').empty();
        $('#add-new-response').show();
    },

    addImageLinkInput: function(){
        var link_images = this.$('.civi-link-images').length;
        if (link_images > 20 ) {
            Materialize.toast("Don't think you need any more...", 5000);
        } else {
            this.$('.image-link-list').append('<input type="text" class="civi-link-images" placeholder="Paste your image link here..."/>');
        }

    },

    previewImageNames: function(e) {
        var attachment_input = this.$('#response_attachment_image');
        var uploaded_images = attachment_input[0].files;
        var $previewlist = this.$('.file-preview');
        $previewlist.empty();
        // File Upload Images
        _.each(uploaded_images, function(img_file){
            $previewlist.append("<div class=\"link-lato gray-text preview-item \">"+img_file.name+"</div>");
        }, this);

        // Link Images
        this.attachment_links = [];
        var link_images = $('.civi-link-images');
        _.each(link_images, function(img_link){
            var link_value = img_link.value.trim();
            if (link_value){
                $previewlist.append("<div class=\"link-lato gray-text preview-item \">"+link_value+"</div>");
                this.attachment_links.push(link_value);
            }
        }, this);

        // Total images count
        var image_total = uploaded_images.length + this.attachment_links.length;
        if (image_total === 0) {
            $previewlist.prepend("<div>No Images</div>");
        } else if (image_total === 1) {
            $previewlist.prepend("<div>1 Image</div>");
        } else {
            $previewlist.prepend("<div>" + image_total + " Images</div>");
        }

        this.attachmentCount = image_total;

    },

    createResponse: function (e) {
        var _this = this;
        this.$(e.currentTarget).addClass('disabled').attr('disabled', true);
        var title = this.$('#response-title').val(),
            body = this.$('#response-body').val(),
            related_civi, c_type;
        if (this.rebuttal_ref) {
            c_type = 'rebuttal';
            related_civi = this.rebuttal_ref;
        } else {
            c_type = 'response';
            related_civi = this.options.parentView.currentCivi;
        }
        if (title && body) {
            $.ajax({
                url: '/api/new_civi/',
                type: 'POST',
                data: {
                    title: title,
                    body: body,
                    c_type: c_type,
                    thread_id: this.model.threadId,
                    related_civi: related_civi
                },
                success: function (response) {
                    var attachment_input = _this.$('#response_attachment_image');
                    var uploaded_images = attachment_input[0].files;
                    if (_this.attachmentCount > 0) {
                        var formData = new FormData(_this.$('#response_attachment_image_form')[0]);
                        formData.set('civi_id', response.data.id);
                        if (_this.attachment_links.length){
                            _.each(_this.attachment_links, function(img_link){
                                formData.append('attachment_links[]', img_link);
                            });
                        }

                        $.ajaxSetup({
                            beforeSend: function(xhr, settings) {
                                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                                }
                            }
                        });

                        $.ajax({
                            url: '/api/upload_images/',
                            type: 'POST',
                            success: function (response2) {
                                Materialize.toast('New response created.', 5000);
                                _this.options.parentView.responseCollection.fetch();
                                _this.options.parentView.renderResponses();
                                _this.$el.empty();
                            },
                            error: function(e){
                                Materialize.toast('Response was created but images could not be uploaded', 5000);
                                // _this.$(e.currentTarget).removeClass('disabled').attr('disabled', false);
                                _this.options.parentView.responseCollection.fetch();
                                _this.options.parentView.renderResponses();
                                _this.$el.empty();
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
                        _this.$el.empty();
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
    el: '.thread-wiki-holder',
    template: _.template($('#edit-wiki-template').html()),
    initialize: function (options) {
        this.options = options || {};
        this.threadId = options.threadId;
        this.parentView = options.parentView;
        this.removeImage = false;
        this.imageMode = "";
        this.render();
    },

    render: function () {
        this.$el.empty().append(this.template());
        this.$('#thread-image-forms').addClass('hide');
        cw.materializeShit();
    },

    events: {
        'click .create-new-response': 'createResponse',
        'click .cancel-thread': 'cancelEdit',
        'click .delete-previous-image': 'showImageForm',
        'click .use-previous-image': 'hideImageForm',
        'click .edit-thread': 'editThread',
        'click #image-from-computer': 'showImageUploadForm',
        'click #image-from-link': 'showImageLinkForm',
        'change #thread-location': 'showStates',
    },

    show: function () {
        this.$('.edit-thread-modal').openModal();
    },

    hide: function () {
        this.$('.edit-thread-modal').closeModal();
    },

    cancelEdit: function () {
        this.parentView.threadWikiRender();
    },

    showImageForm: function () {
        this.$('#thread-image-forms').removeClass('hide');
        this.$('.previous-image').addClass('hide');
        this.removeImage = true;
    },

    hideImageForm: function () {
        this.$('#thread-image-forms').addClass('hide');
        this.$('.previous-image').removeClass('hide');
        this.removeImage = false;
    },
    showImageUploadForm: function () {
        this.imageMode="upload";
        this.$('#attachment_image_form').removeClass('hide');
        this.$('#link-image-form').addClass('hide');
    },
    showImageLinkForm: function () {
        this.imageMode="link";
        this.$('#attachment_image_form').addClass('hide');
        this.$('#link-image-form').removeClass('hide');
    },

    editThread: function (e) {
        var _this = this;
        _this.$(e.currentTarget).addClass('disabled').attr('disabled', true);

        var title = this.$el.find('#thread-title').val().trim();
        var summary = this.$el.find('#thread-body').val().trim();
        var category_id = this.$el.find('#thread-category').val();

        var thread_id = this.threadId;
        
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
                    var img_url = _this.$('#link-image-form').val().trim();
                    if (_this.removeImage) {
                        // if file
                        if (_this.imageMode==="upload" && file){
                            var formData = new FormData(_this.$('#attachment_image_form')[0]);
                            formData.set('thread_id', response.data.thread_id);

                            $.ajaxSetup({
                                beforeSend: function(xhr, settings) {
                                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                                    }
                                }
                            });

                            $.ajax({
                                url: '/api/upload_image/',
                                type: 'POST',
                                success: function (response2) {
                                    Materialize.toast('Saved changes', 5000);
                                    // _this.hide();


                                    new_data = response.data;
                                    _this.parentView.model.set('title', new_data.title);
                                    _this.parentView.model.set('summary', new_data.summary);
                                    _this.parentView.model.set('category', new_data.category);
                                    _this.parentView.model.set('image', response2.image);
                                    _this.parentView.threadWikiRender();
                                    _this.parentView.threadNavRender();

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
                        } else if (_this.imageMode==="link" && img_url){

                            $.ajax({
                                url: '/api/upload_image/',
                                type: 'POST',
                                data: {
                                    csrfmiddlewaretoken: csrftoken,
                                    link: img_url,
                                    thread_id: response.data.thread_id
                                },
                                success: function (response2) {
                                    Materialize.toast('Saved changes', 5000);
                                    _this.hide();


                                    new_data = response.data;
                                    _this.parentView.model.set('title', new_data.title);
                                    _this.parentView.model.set('summary', new_data.summary);
                                    _this.parentView.model.set('category', new_data.category);
                                    _this.parentView.model.set('image', response2.image);
                                    _this.parentView.threadWikiRender();
                                    _this.parentView.threadNavRender();
                                },
                                error: function(e){
                                    Materialize.toast('ERROR: Image could not be uploaded', 5000);
                                    Materialize.toast(e.statusText, 5000);
                                    _this.$(e.currentTarget).removeClass('disabled').attr('disabled', false);
                                }
                            });
                        }
                        else { // Remove image
                            $.ajax({
                                url: '/api/upload_image/',
                                type: 'POST',
                                data: {
                                    csrfmiddlewaretoken: csrftoken,
                                    remove: true,
                                    thread_id: response.data.thread_id
                                },
                                success: function (response2) {
                                    Materialize.toast('Saved changes', 5000);
                                    // _this.hide();

                                    new_data = response.data;
                                    _this.parentView.model.set('title', new_data.title);
                                    _this.parentView.model.set('summary', new_data.summary);
                                    _this.parentView.model.set('category', new_data.category);
                                    _this.parentView.model.set('image', response2.image);
                                    _this.parentView.threadWikiRender();
                                    _this.parentView.threadNavRender();
                                },
                                error: function(e){
                                    Materialize.toast('ERROR: Image could not be uploaded', 5000);
                                    Materialize.toast(e.statusText, 5000);
                                    _this.$(e.currentTarget).removeClass('disabled').attr('disabled', false);
                                }
                            });
                        }

                    } else {
                        Materialize.toast('Saved changes', 5000);
                        // _this.hide();

                        // New Data
                        new_data = response.data;
                        _this.parentView.model.set('title', new_data.title);
                        _this.parentView.model.set('summary', new_data.summary);
                        _this.parentView.model.set('category',new_data.category);
                        _this.parentView.threadWikiRender();
                        _this.parentView.threadNavRender();
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

cw.OutlineView = BB.View.extend({});

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
            id : 'civi_links',
            displayField: 'title',
            expandOnFocus: true,
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
        if (c_type == 'cause') {
            linkableCivis = _this.civis.where({type:'problem'});
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

        this.ms.setData(msdata);

        return this;
    },
});

cw.ThreadView = BB.View.extend({
    el: '#thread',
    template: _.template($('#thread-template').html()),
    wikiTemplate: _.template($('#thread-wiki-template').html()),
    bodyTemplate: _.template($('#thread-body-template').html()),
    navTemplate: _.template($('#thread-nav-template').html()),
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
        this.threadNavRender();

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

    // Renders thread navbar element independently of main body.
    // Useful for updating after thread edits are saved.
    threadNavRender: function () {
      var _this = this;
      var navRenderData = {
          is_draft: this.is_draft,
      };
      this.$('.thread-nav').empty().append(this.navTemplate(navRenderData));
      this.$('.main-thread').on('scroll', function (e) {
            _this.processCiviScroll();
      });
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
            // render with mock data to prevent errors
            var mockData = {
                is_draft: undefined,
                count: 0,
                problems: [],
                causes: [],
                solutions: []
            }
            
            this.$('#civi-outline').empty().append(this.outlineTemplate(mockData));
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

        var scrollPadding = 100;
        
        if (this.civiLocations.length) {
            // Padding so you can scroll and track the last civi element;
            scrollPadding = this.$('.main-thread').height() - this.civiLocations[this.civiLocations.length-1].height;
        }
        
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
    },

    civiRenderHelper: function(civi){
        var is_draft = civi.is_draft;
        var can_edit = civi.get('author').username == this.username ? true : false;
        this.$('#thread-'+civi.get('type')+'s').append(new cw.CiviView({model: civi, can_edit: can_edit, is_draft: is_draft, parentView: this}).el);

    },

    renderVotes: function() {
        var _this = this;
        var savedVotes = this.model.get('user_votes');
        _.each(savedVotes, function(v){
            this.$('#civi-'+ v.civi_id).find("." +v.activity_type).addClass('current');
        });
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

        this.$('.civi-card').each(function (idx, civi) {
            var $civi = $(civi),
                $civiTop = $civi.position().top + scrollPos - threadPos;
            _this.civiLocations.push({top: $civiTop, bottom: $civiTop + $civi.height(), height: $civi.height(), target: $civi, id: $civi.attr('data-civi-id')});
        });
    },

    processCiviScroll: function () {
        var _this = this;
        var scrollPosition = this.$('.main-thread').scrollTop();
        // 1. Check if there are any civis. No tracking if none
        if (this.civis.length === 0){
            return;
        }

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
                csrfmiddlewaretoken: csrftoken,
                thread_id: _this.model.threadId,
                title: _this.model.attributes.title,
                summary: _this.model.attributes.summary,
                // Why is categories an array, when only one category is ever chosen?
                category_id: _this.model.attributes.categories[0].id,
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

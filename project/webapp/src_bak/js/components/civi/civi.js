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
        // 'click .favorite': 'clickFavorite',
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
        // 'click .civi-grab-link': 'grabLink',
        // vote
        // changevote

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
        console.log(new_type);
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
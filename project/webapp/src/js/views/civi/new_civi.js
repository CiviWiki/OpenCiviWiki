cw.NewCiviView = BB.View.extend({
    el: '#new-civi-box',
    template: _.template($('#new-civi-template').html()),

    initialize: function (options) {
        this.options = options || {};
    },

    render: function () {
        this.$el.empty().append(this.template());
        // $('.responses').height($('#new-civi-box').height() + $('.responses-box').height());

        this.magicSuggestView = new cw.LinkSelectView({$el: this.$('#magicsuggest'), civis: this.options.parentView.civis});

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
        // $('.responses').height($('.responses-box').height());
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
                    title: title,
                    body: body,
                    c_type: c_type,
                    thread_id: _this.model.threadId,
                    links: links
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
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
    //
    // show: function () {
    //     this.$('.new-response-modal').openModal();
    // },
    //
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
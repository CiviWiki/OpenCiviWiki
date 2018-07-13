import { View } from 'backbone.marionette';

const NewResponseView = View.extend({
  el: '#new-response-box',
  template: _.template($('#new-response-template').html()),
  initialize(options) {
    this.options = options || {};
    this.rebuttal_ref = '';
  },

  render() {
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
  hide() {
    $('#new-response-box').empty();
    $('#add-new-response').show();
  },

  addImageLinkInput() {
    const link_images = this.$('.civi-link-images').length;
    if (link_images > 20) {
      Materialize.toast("Don't think you need any more...", 5000);
    } else {
      this.$('.image-link-list').append(
        '<input type="text" class="civi-link-images" placeholder="Paste your image link here..."/>',
      );
    }
  },

  previewImageNames(e) {
    const attachment_input = this.$('#response_attachment_image');
    const uploaded_images = attachment_input[0].files;
    const $previewlist = this.$('.file-preview');
    $previewlist.empty();
    // File Upload Images
    _.each(
      uploaded_images,
      (img_file) => {
        $previewlist.append(
          `<div class="link-lato gray-text preview-item ">${img_file.name}</div>`,
        );
      },
      this,
    );

    // Link Images
    this.attachment_links = [];
    const link_images = $('.civi-link-images');
    _.each(
      link_images,
      function (img_link) {
        const link_value = img_link.value.trim();
        if (link_value) {
          $previewlist.append(
            `<div class="link-lato gray-text preview-item ">${link_value}</div>`,
          );
          this.attachment_links.push(link_value);
        }
      },
      this,
    );

    // Total images count
    const image_total = uploaded_images.length + this.attachment_links.length;
    if (image_total === 0) {
      $previewlist.prepend('<div>No Images</div>');
    } else if (image_total === 1) {
      $previewlist.prepend('<div>1 Image</div>');
    } else {
      $previewlist.prepend(`<div>${image_total} Images</div>`);
    }

    this.attachmentCount = image_total;
  },

  createResponse(e) {
    const _this = this;
    this.$(e.currentTarget)
      .addClass('disabled')
      .attr('disabled', true);
    const title = this.$('#response-title').val();


    const body = this.$('#response-body').val();


    let related_civi;


    let c_type;
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
          title,
          body,
          c_type,
          thread_id: this.model.threadId,
          related_civi,
        },
        success(response) {
          const attachment_input = _this.$('#response_attachment_image');
          const uploaded_images = attachment_input[0].files;
          if (_this.attachmentCount > 0) {
            const formData = new FormData(_this.$('#response_attachment_image_form')[0]);
            formData.set('civi_id', response.data.id);
            if (_this.attachment_links.length) {
              _.each(_this.attachment_links, (img_link) => {
                formData.append('attachment_links[]', img_link);
              });
            }
            $.ajax({
              url: '/api/upload_images/',
              type: 'POST',
              success(response2) {
                Materialize.toast('New response created.', 5000);
                _this.options.parentView.responseCollection.fetch();
                _this.options.parentView.renderResponses();
                _this.$el.empty();
              },
              error(e) {
                Materialize.toast('Response was created but images could not be uploaded', 5000);
                // _this.$(e.currentTarget).removeClass('disabled').attr('disabled', false);
                _this.options.parentView.responseCollection.fetch();
                _this.options.parentView.renderResponses();
                _this.$el.empty();
              },
              data: formData,
              cache: false,
              contentType: false,
              processData: false,
            });
          } else {
            Materialize.toast('New response created.', 5000);
            _this.options.parentView.responseCollection.fetch();
            _this.options.parentView.renderResponses();
            _this.$el.empty();
          }
        },
        error() {
          Materialize.toast('Could not create response', 5000);
          _this
            .$(e.currentTarget)
            .removeClass('disabled')
            .attr('disabled', false);
        },
      });
    } else {
      Materialize.toast('Please input all fields.', 5000);
      _this
        .$(e.currentTarget)
        .removeClass('disabled')
        .attr('disabled', false);
    }
  },
});
export default NewResponseView;

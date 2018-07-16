import { View } from 'backbone.marionette';
import baseTemplate from 'Templates/components/Thread/Civi/new_response.html';

const NewResponseView = View.extend({
  el: '#new-response-box',
  template: baseTemplate,

  initialize() {
    this.rebuttal_ref = '';
  },

  onRender() {
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
  hide() {
    $('#new-response-box').empty();
    $('#add-new-response').show();
  },

  addImageLinkInput() {
    const linkImages = this.$('.civi-link-images').length;
    if (linkImages > 20) {
      M.toast({ html: "Don't think you need any more..." });
    } else {
      this.$('.image-link-list').append(
        '<input type="text" class="civi-link-images" placeholder="Paste your image link here..."/>',
      );
    }
  },

  previewImageNames() {
    const attachmentInput = this.$('#response_attachment_image');
    const uploadedImages = attachmentInput[0].files;
    const $previewlist = this.$('.file-preview');
    $previewlist.empty();
    // File Upload Images
    _.each(
      uploadedImages,
      (ImageFile) => {
        $previewlist.append(
          `<div class="link-lato gray-text preview-item ">${ImageFile.name}</div>`,
        );
      },
      this,
    );

    // Link Images
    this.attachment_links = [];
    const linkImages = $('.civi-link-images');
    _.each(
      linkImages,
      (imageLink) => {
        const linkValue = imageLink.value.trim();
        if (linkValue) {
          $previewlist.append(`<div class="link-lato gray-text preview-item ">${linkValue}</div>`);
          this.attachment_links.push(linkValue);
        }
      },
      this,
    );

    // Total images count
    const imageTotal = uploadedImages.length + this.attachment_links.length;
    if (imageTotal === 0) {
      $previewlist.prepend('<div>No Images</div>');
    } else if (imageTotal === 1) {
      $previewlist.prepend('<div>1 Image</div>');
    } else {
      $previewlist.prepend(`<div>${imageTotal} Images</div>`);
    }

    this.attachmentCount = imageTotal;
  },

  createResponse(event) {
    const view = this;
    this.$(event.currentTarget)
      .addClass('disabled')
      .attr('disabled', true);
    const responseTitle = this.$('#response-title').val();
    const responseBody = this.$('#response-body').val();

    let relatedCivi;
    let civiType;
    if (this.rebuttal_ref) {
      civiType = 'rebuttal';
      relatedCivi = this.rebuttal_ref;
    } else {
      civiType = 'response';
      relatedCivi = this.options.parentView.currentCivi;
    }
    if (responseTitle && responseBody) {
      $.ajax({
        url: '/api/new_civi/',
        type: 'POST',
        data: {
          title: responseTitle,
          body: responseBody,
          c_type: civiType,
          thread_id: this.model.id,
          related_civi: relatedCivi,
        },
        success(response) {
          if (view.attachmentCount > 0) {
            const formData = new FormData(view.$('#response_attachment_image_form')[0]);
            formData.set('civi_id', response.data.id);
            if (view.attachment_links.length) {
              _.each(view.attachment_links, (imageLink) => {
                formData.append('attachment_links[]', imageLink);
              });
            }
            $.ajax({
              url: '/api/upload_images/',
              type: 'POST',
              success() {
                M.toast({ html: 'New response created.' });
                view.options.parentView.responseCollection.fetch();
                view.options.parentView.renderResponses();
                view.$el.empty();
              },
              error() {
                M.toast({ html: 'Response was created but images could not be uploaded' });
                view.options.parentView.responseCollection.fetch();
                view.options.parentView.renderResponses();
                view.$el.empty();
              },
              data: formData,
              cache: false,
              contentType: false,
              processData: false,
            });
          } else {
            M.toast({ html: 'New response created.' });
            view.options.parentView.responseCollection.fetch();
            view.options.parentView.renderResponses();
            view.$el.empty();
          }
        },
        error() {
          M.toast({ html: 'Could not create response' });
          view
            .$(event.currentTarget)
            .removeClass('disabled')
            .attr('disabled', false);
        },
      });
    } else {
      M.toast({ html: 'Please input all fields.' });
      view
        .$(event.currentTarget)
        .removeClass('disabled')
        .attr('disabled', false);
    }
  },
});
export default NewResponseView;

import { View } from 'backbone.marionette';
import baseTemplate from 'Templates/components/Thread/new_civi.html';
import { Civi } from '../../models';
import LinkSelectView from './LinkSelect';
import CiviView from './Civi';

const NewCiviView = View.extend({
  el: '#new-civi-box',
  template: baseTemplate,

  onRender() {
    this.$el.empty().append(this.template());

    this.magicSuggestView = new LinkSelectView({
      $el: this.$('#magicsuggest'),
      civis: this.options.parentView.civis,
    });

    this.$('.edit-links').addClass('hide');
    this.$('#magicsuggest').addClass('hide');

    this.attachment_links = [];
    this.attachmentCount = 0;
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
    const attachmentInput = this.$('#id_attachment_image');
    const uploadedImages = attachmentInput[0].files;
    const $previewlist = this.$('.file-preview');
    $previewlist.empty();
    // File Upload Images
    _.each(
      uploadedImages,
      (imageFile) => {
        $previewlist.append(
          `<div class="link-lato gray-text preview-item ">${imageFile.name}</div>`,
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
    const imageTotalCount = uploadedImages.length + this.attachment_links.length;
    if (imageTotalCount === 0) {
      $previewlist.prepend('<div>No Images</div>');
    } else if (imageTotalCount === 1) {
      $previewlist.prepend('<div>1 Image</div>');
    } else {
      $previewlist.prepend(`<div>${imageTotalCount} Images</div>`);
    }

    this.attachmentCount = imageTotalCount;
  },

  cancelCivi() {
    this.$el.empty();
  },

  createCivi(event) {
    const view = this;
    const newTitle = this.$el.find('#civi-title').val();
    const newBody = this.$el.find('#civi-body').val();
    const civiType = this.$el.find('.civi-types > .current').val();
    const msLinks = this.magicSuggestView.ms.getValue();

    this.$(event.currentTarget)
      .addClass('disabled')
      .attr('disabled', true);

    if (newTitle && newBody && civiType) {
      if (msLinks.length === 0) {
        if (civiType === 'cause') {
          M.toast({
            html:
              'A CAUSE Civi must be linked to a PROBLEM Civi. If it is only linked to a solution it will not appear',
          });
          this.$(event.currentTarget)
            .removeClass('disabled')
            .attr('disabled', false);
          return;
        }
        if (civiType === 'solution') {
          M.toast({ html: 'A SOLUTION Civi must be linked to a CAUSE Civi' });
          this.$(event.currentTarget)
            .removeClass('disabled')
            .attr('disabled', false);
          return;
        }
      }
      $.ajax({
        url: '/api/new_civi/',
        type: 'POST',
        data: {
          title: newTitle,
          body: newBody,
          c_type: civiType,
          thread_id: view.model.threadId,
          links: msLinks,
        },
        success(response) {
          const newCiviData = response.data;
          const newCivi = new Civi(newCiviData);
          const canEdit = newCivi.get('author').username === view.options.parentView.username;

          //   const attachmentInput = view.$('#id_attachment_image');
          //   const uploadedImages = attachmentInput[0].files;
          if (view.attachmentCount > 0) {
            const formData = new FormData(view.$('#attachment_image_form')[0]);
            formData.set('civi_id', response.data.id);
            if (view.attachment_links.length) {
              _.each(view.attachment_links, (imageLink) => {
                formData.append('attachment_links[]', imageLink);
              });
            }

            $.ajax({
              url: '/api/upload_images/',
              type: 'POST',
              success(imageResponse) {
                M.toast({ html: 'New civi created.' });
                newCivi.set('attachments', imageResponse.attachments);

                $(`#thread-${civiType}s`).append(
                  new CiviView({
                    model: newCivi,
                    can_edit: canEdit,
                    parentView: view.options.parentView,
                  }).el,
                );
                view.options.parentView.civis.add(newCivi);

                view.options.parentView.initRecommended();
                view.options.parentView.renderBodyContents();
                view.$el.empty();

                $('body').css({ overflow: 'hidden' });
              },
              error() {
                M.toast({ html: 'Civi was created but one or more images could not be uploaded' });
                $(`#thread-${civiType}s`).append(
                  new CiviView({
                    model: newCivi,
                    can_edit: canEdit,
                    parentView: view.options.parentView,
                  }).el,
                );
                view.options.parentView.civis.add(newCivi);

                view.options.parentView.initRecommended();
                view.options.parentView.renderBodyContents();

                view.$el.empty();

                $('body').css({ overflow: 'hidden' });
              },
              data: formData,
              cache: false,
              contentType: false,
              processData: false,
            });
          } else {
            M.toast({ html: 'New civi created.' });
            $(`#thread-${civiType}s`).append(
              new CiviView({
                model: newCivi,
                can_edit: canEdit,
                parentView: view.options.parentView,
              }).el,
            );
            view.options.parentView.civis.add(newCivi);

            const parentLinks = newCivi.get('links');
            _.each(
              parentLinks,
              (parentId) => {
                const parentCivi = view.options.parentView.civis.get(parentId);
                if (parentCivi) {
                  const previousLinks = parentCivi.get('links');
                  previousLinks.push(newCivi.id);
                  parentCivi.set('links', previousLinks);
                }
              },
              this,
            );
            view.options.parentView.initRecommended();
            view.options.parentView.renderBodyContents();
            view.$el.empty();
          }
        },
        error() {
          M.toast({ html: 'Could not create Civi' });
          view
            .$(event.currentTarget)
            .removeClass('disabled')
            .attr('disabled', false);
        },
      });
    } else {
      M.toast({ html: 'Please input all fields.' });
      this.$(event.currentTarget)
        .removeClass('disabled')
        .attr('disabled', false);
    }
  },

  clickType(event) {
    const $this = $(event.target).closest('.civi-type-button');

    $this.addClass('current');
    $this.siblings().removeClass('current');

    const civiType = this.$el.find('.civi-types > .current').val();

    if (civiType === 'problem') {
      this.$('.edit-links').addClass('hide');
      this.$('#magicsuggest').addClass('hide');
    } else {
      this.$('.edit-links').removeClass('hide');
      this.$('#magicsuggest').removeClass('hide');
      this.magicSuggestView.setLinkableData(civiType);
      this.magicSuggestView.ms.clear();
    }
  },
});
export default NewCiviView;

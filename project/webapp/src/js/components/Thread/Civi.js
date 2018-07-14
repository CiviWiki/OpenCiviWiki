import { View } from 'backbone.marionette';
import baseTemplate from 'Templates/components/Thread/civi.html';
import LinkSelectView from './LinkSelect';

const CiviView = View.extend({
  template: baseTemplate,

  initialize() {
    this.can_edit = this.getOption('can_edit');
    this.is_draft = this.getOption('is_draft');
    this.can_respond = this.getOption('can_respond');
    this.parentView = this.getOption('parentView');
    this.civis = this.parentView.civis;
    this.model.set('view', this);
    this.renderView();
  },

  renderView() {
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
    const view = this;
    const attachmentInput = this.$('#id_attachment_image');
    const uploadedImages = attachmentInput[0].files;
    const $previewlist = this.$('.file-preview');
    $previewlist.empty();
    // File Upload Images
    _.each(uploadedImages, (imageFile) => {
      $previewlist.append(`<div class="link-lato gray-text preview-item ">${imageFile.name}</div>`);
    });

    // Link Images
    this.attachmentLinks = [];
    const linkImages = $('.civi-link-images');
    _.each(linkImages, (imageLink) => {
      const linkValue = imageLink.value.trim();
      if (linkValue) {
        $previewlist.append(`<div class="link-lato gray-text preview-item ">${linkValue}</div>`);
        view.attachmentLinks.push(linkValue);
      }
    });

    // Total images count
    const imageTotal = uploadedImages.length + this.attachmentLinks.length;
    if (imageTotal === 0) {
      $previewlist.prepend('<div>No Images</div>');
    } else if (imageTotal === 1) {
      $previewlist.prepend('<div>1 Image</div>');
    } else {
      $previewlist.prepend(`<div>${imageTotal} Images</div>`);
    }

    this.attachmentCount = imageTotal;
  },

  showImageForm() {
    this.$('.edit-images').removeClass('hide');
    this.$('#add-more-images').addClass('hide');
  },

  viewImageModal(event) {
    event.stopPropagation();
    const imageSource = $(event.currentTarget).attr('src');
    const $modal = $('#civi-image-modal');
    $('#civi-image-big').attr('src', imageSource);
    $modal.openModal();
  },

  grabLink(event) {
    event.stopPropagation();
    M.toast({ html: 'Civi link copied to clipboard.' });
  },

  clickRating(event) {
    event.stopPropagation();
    const view = this;
    const $this = $(event.currentTarget);

    const rating = $this.data('rating');
    const civiId = $(event.currentTarget)
      .closest('.civi-card')
      .data('civi-id');

    if (rating && civiId) {
      $.ajax({
        url: '/api/rate_civi/',
        type: 'POST',
        data: {
          civi_id: civiId,
          rating,
        },
        success(response) {
          M.toast({ html: 'Voted!' });
          let prevVotes = view.parentView.model.get('user_votes');
          const prevVote = _.findWhere(prevVotes, { civiId });
          if (!prevVote) {
            prevVotes.push(response.data);
            view.parentView.model.set('user_votes', prevVotes);
          } else {
            prevVotes = _.reject(prevVotes, v => v.civiId === civiId);
            prevVotes.push(response.data);
            view.parentView.model.set('user_votes', prevVotes);
          }

          if (view.model.get('type') !== 'response' && view.model.get('type') !== 'rebuttal') {
            view.parentView.initRecommended();
            view.parentView.renderBodyContents();
            view.parentView.processCiviScroll();
          }

          view.$('.rating-button').removeClass('current');
          $this.addClass('current');
        },
        error() {
          M.toast({ html: 'Could not vote :(' });
        },
      });
    }
  },

  clickEdit(event) {
    event.stopPropagation();
    this.$('.edit-civi-body').text(this.model.get('body'));
    this.$('.edit-civi-title').val(this.model.get('title'));
    this.$(`#${this.model.get('type')}-${this.model.id}`).prop('checked', true);
    if (this.model.get('type') !== 'response' && this.model.get('type') !== 'rebuttal') {
      this.magicSuggestView = new LinkSelectView({
        $el: this.$(`#magicsuggest-${this.model.id}`),
        civis: this.civis,
      });
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
      this.$(`#magicsuggest-${this.model.id}`).addClass('hide');
    }
  },

  clickNewType(event) {
    const newType = $(event.target)
      .closest("input[type='radio']:checked")
      .val();
    if (newType === 'problem') {
      this.$('.edit-links').addClass('hide');
      this.$(`#magicsuggest-${this.model.id}`).addClass('hide');
    } else {
      this.$('.edit-links').removeClass('hide');
      this.$(`#magicsuggest-${this.model.id}`).removeClass('hide');
    }
    this.magicSuggestView.setLinkableData(newType);
    this.magicSuggestView.ms.clear();
  },

  addRebuttal() {
    this.parentView.newResponseView.rebuttal_ref = this.model.id;
    this.parentView.newResponseView.render();
    this.parentView.newResponseView.show();
  },

  addImageToDeleteList(event) {
    const target = $(event.currentTarget);
    const targetImage = target.data('image-id');
    this.imageRemoveList.push(targetImage);
    target.remove();
  },

  closeEdit(event) {
    event.stopPropagation();
    this.$('.edit-wrapper').addClass('hide');
    this.$('.edit-action').addClass('hide');
    this.$('.text-wrapper').removeClass('hide');
    this.$('.edit').removeClass('hide');
    this.$('.delete').removeClass('hide');
  },

  saveEdit(event) {
    event.stopPropagation();
    const view = this;
    const civiType = this.model.get('type');
    const newBody = this.$('.edit-civi-body')
      .val()
      .trim();

    const newTitle = this.$('.edit-civi-title')
      .val()
      .trim();

    let links;
    if (civiType !== 'response' && civiType !== 'rebuttal') {
      links = this.magicSuggestView.ms.getValue();
    } else {
      links = [];
    }

    let newType = this.$("#civi-type-form input[type='radio']:checked").val();
    if (!newBody || !newTitle) {
      M.toast({ html: 'Please do not leave fields blank' });
      return;
    }
    if (
      this.imageRemoveList.length === 0
      && this.attachmentCount === 0
      && (newBody === this.model.get('body')
        && newTitle === this.model.get('title')
        && _.isEqual(links, this.model.get('links'))
        && newType === this.model.get('type'))
    ) {
      this.closeEdit(event);
      return;
    }
    let data;

    if (civiType === 'response' || civiType === 'rebuttal') {
      newType = civiType;
      data = {
        civi_id: this.model.id,
        title: newTitle,
        body: newBody,
      };
    } else {
      data = {
        civi_id: this.model.id,
        title: newTitle,
        body: newBody,
        links,
        type: newType,
      };
    }

    if (this.imageRemoveList.length) {
      data.image_remove_list = this.imageRemoveList;
    }
    $.ajax({
      url: '/api/edit_civi/',
      type: 'POST',
      data,
      success(response) {
        view.closeEdit(event);
        if (view.attachmentCount > 0) {
          const formData = new FormData(view.$('#attachment_image_form')[0]);
          formData.set('civi_id', view.model.id);
          if (view.attachment_links.length) {
            _.each(view.attachment_links, (imageLink) => {
              formData.append('attachment_links[]', imageLink);
            });
          }

          $.ajax({
            url: '/api/upload_images/',
            type: 'POST',
            success(imageResponse) {
              M.toast({ html: 'Saved.' });

              // Set the models with new data and rerender
              view.model.set('title', newTitle);
              view.model.set('body', newBody);
              view.model.set('links', links);
              view.model.set('type', newType);
              view.model.set('attachments', imageResponse.attachments);
              view.model.set('score', response.score);
              if (view.magicSuggestView) {
                view.magicSuggestView.remove();
              }

              view.render();

              if (view.model.get('type') !== 'response' && view.model.get('type') !== 'rebuttal') {
                const parentLinks = view.model.get('links');
                _.each(
                  parentLinks,
                  (parentId) => {
                    const parentCivi = view.options.parentView.civis.get(parentId);
                    if (parentCivi) {
                      const prevLinks = parentCivi.get('links');
                      prevLinks.push(view.model.id);
                      parentCivi.set('links', prevLinks);
                    }
                  },
                  this,
                );

                view.parentView.initRecommended();
                view.parentView.renderBodyContents();
                view.parentView.processCiviScroll();
              }
            },
            error(imageResponse) {
              M.toast({
                html: 'Civi was edited but one or more images could not be uploaded',
              });

              // Set the models with new data and rerender
              view.model.set('title', newTitle);
              view.model.set('body', newBody);
              view.model.set('links', links);
              view.model.set('type', newType);
              view.model.set('attachments', imageResponse.attachments);
              view.model.set('score', response.score);
              if (view.magicSuggestView) {
                view.magicSuggestView.remove();
              }

              view.render();

              if (view.model.get('type') !== 'response' && view.model.get('type') !== 'rebuttal') {
                const parentLinks = view.model.get('links');
                _.each(
                  parentLinks,
                  (parentId) => {
                    const parentCivi = view.options.parentView.civis.get(parentId);
                    if (parentCivi) {
                      const prevLinks = parentCivi.get('links');
                      prevLinks.push(view.model.id);
                      parentCivi.set('links', prevLinks);
                    }
                  },
                  this,
                );

                view.parentView.initRecommended(); // THISTHIS
                view.parentView.renderBodyContents();
                view.parentView.processCiviScroll();
              }
            },
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
          });
        } else {
          M.toast({ html: 'Saved' });

          // Clean up previous links
          if (view.model.get('type') !== 'response' && view.model.get('type') !== 'rebuttal') {
            const origLinks = view.model.get('links');
            _.each(
              origLinks,
              (parentId) => {
                const parentCivi = view.options.parentView.civis.get(parentId);
                if (parentCivi) {
                  const prevLinks = parentCivi.get('links');
                  const cleaned = _.without(prevLinks, view.model.id);
                  parentCivi.set('links', cleaned);
                }
              },
              this,
            );
          }
          // Set the models with new data and rerender
          view.model.set('title', newTitle);
          view.model.set('body', newBody);
          view.model.set('links', links);
          view.model.set('type', newType);
          view.model.set('attachments', response.attachments);
          view.model.set('score', response.score);
          if (view.magicSuggestView) {
            view.magicSuggestView.remove();
          }

          view.render();

          if (view.model.get('type') !== 'response' && view.model.get('type') !== 'rebuttal') {
            const parentLinks = view.model.get('links');
            _.each(
              parentLinks,
              (parentId) => {
                const parentCivi = view.options.parentView.civis.get(parentId);
                if (parentCivi) {
                  const prevLinks = parentCivi.get('links');
                  prevLinks.push(view.model.id);
                  parentCivi.set('links', prevLinks);
                }
              },
              this,
            );

            view.parentView.initRecommended();
            view.parentView.renderBodyContents();
            view.parentView.processCiviScroll();
          }
        }
      },
      error() {
        M.toast({ html: 'Could not edit the civi' });
        view.closeEdit(event);
        view.render();
      },
    });
  },

  deleteEdit(event) {
    const view = this;
    event.stopPropagation();

    $.ajax({
      url: '/api/delete_civi/',
      type: 'POST',
      data: {
        civi_id: this.model.id,
      },
      success() {
        M.toast({ html: 'Deleted Civi succssfully' });
        _.each(view.model.get('links'), (link) => {
          const linkedCivi = view.civis.findWhere({ id: link });
          const prevLinks = linkedCivi.get('links');
          const newLinks = _.without(prevLinks, view.model.id);
          linkedCivi.set('links', newLinks);
        });

        view.civis.remove(view.model);
        view.remove();
        view.parentView.initRecommended();
        view.parentView.renderBodyContents();
        view.parentView.processCiviScroll();
      },
      error() {
        M.toast({ html: 'Could not delete the civi' });
      },
    });
  },
});

export default CiviView;

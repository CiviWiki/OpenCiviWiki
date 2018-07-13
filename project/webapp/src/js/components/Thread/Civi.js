import { View } from 'backbone.marionette';

const CiviView = View.extend({
  template: _.template($('#civi-template').html()),

  initialize(options) {
    this.options = options || {};
    this.can_edit = options.can_edit;
    this.is_draft = options.is_draft;
    this.can_respond = options.can_respond;
    this.parentView = options.parentView;
    this.civis = this.parentView.civis;
    this.model.set('view', this);
    this.render();
  },

  render() {
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
    const attachment_input = this.$('#id_attachment_image');
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

  showImageForm(e) {
    // HEREHERE
    this.$('.edit-images').removeClass('hide');
    this.$('#add-more-images').addClass('hide');
  },

  viewImageModal(e) {
    const img_src = $(e.currentTarget).attr('src');
    const $modal = $('#civi-image-modal');
    $('#civi-image-big').attr('src', img_src);
    $modal.openModal();
    e.stopPropagation();
  },
  // clean() function
  clickFavorite(e) {
    const _this = this;

    if ($this.text() === 'star_border') {
      $.ajax({
        url: '/api/favorite_civi/',
        type: 'POST',
        data: {
          civi_id: this.model.id,
        },
        success(response) {
          Materialize.toast('Favorited Civi', 5000);
          $this.text('star');
        },
        error(r) {
          Materialize.toast('Could not favor the civi', 5000);
        },
      });
    } else {
      $.ajax({
        url: '/api/favorite_civi/',
        type: 'POST',
        data: {
          civi_id: this.model.id,
        },
        success(response) {
          Materialize.toast('Favorited Civi', 5000);
        },
        error(r) {
          Materialize.toast('Could not favor the civi', 5000);
        },
      });
      $this.text('star_border');
    }
  },

  grabLink() {
    e.stopPropagation();
    Materialize.toast('Civi link copied to clipboard.', 1500);
  },

  clickRating(e) {
    e.stopPropagation();
    const _this = this;
    const $this = $(e.currentTarget);

    const rating = $this.data('rating');
    const civi_id = $(e.currentTarget)
      .closest('.civi-card')
      .data('civi-id');

    // if (this.can_edit) {
    //     Materialize.toast('Trying to vote on your own civi? :}', 5000);
    //     return;
    // }
    if (rating && civi_id) {
      $.ajax({
        url: '/api/rate_civi/',
        type: 'POST',
        data: {
          civi_id,
          rating,
        },
        success(response) {
          Materialize.toast('Voted!', 5000);
          // var score = $this.find('.rate-value');
          // var new_vote = parseInt(score.text())+ 1;
          // score.text(new_vote);
          console.log(response.data);
          let prev_votes = _this.parentView.model.get('user_votes');
          const prev_vote = _.findWhere(prev_votes, { civi_id });
          if (!prev_vote) {
            prev_votes.push(response.data);
            _this.parentView.model.set('user_votes', prev_votes);
          } else {
            prev_votes = _.reject(prev_votes, v => v.civi_id === civi_id);
            prev_votes.push(response.data);
            _this.parentView.model.set('user_votes', prev_votes);
          }

          if (_this.model.get('type') != 'response' && _this.model.get('type') != 'rebuttal') {
            _this.parentView.initRecommended(); // THISTHIS
            _this.parentView.renderBodyContents();
            _this.parentView.processCiviScroll();
          }

          _this.$('.rating-button').removeClass('current');
          $this.addClass('current');
        },
        error(r) {
          Materialize.toast('Could not vote :(', 5000);
        },
      });
    }
  },

  clickEdit(e) {
    e.stopPropagation();
    // Populate with data TODO: move to a template
    this.$('.edit-civi-body').text(this.model.get('body'));
    this.$('.edit-civi-title').val(this.model.get('title'));
    this.$(`#${this.model.get('type')}-${this.model.id}`).prop('checked', true);
    if (this.model.get('type') != 'response' && this.model.get('type') != 'rebuttal') {
      this.magicSuggestView = new cw.LinkSelectView({
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

  clickNewType(e) {
    const new_type = $(e.target)
      .closest("input[type='radio']:checked")
      .val();
    // var new_type = $("#civi-type-form input[type='radio']:checked").val();
    if (new_type === 'problem') {
      this.$('.edit-links').addClass('hide');
      this.$(`#magicsuggest-${this.model.id}`).addClass('hide');
    } else {
      this.$('.edit-links').removeClass('hide');
      this.$(`#magicsuggest-${this.model.id}`).removeClass('hide');
    }
    this.magicSuggestView.setLinkableData(new_type);
    this.magicSuggestView.ms.clear();
  },

  addRebuttal() {
    this.parentView.newResponseView.rebuttal_ref = this.model.id;
    this.parentView.newResponseView.render();
    this.parentView.newResponseView.show();
  },

  addImageToDeleteList(e) {
    const target = $(e.currentTarget);
    const target_image = target.data('image-id');

    this.imageRemoveList.push(target_image);
    target.remove();
  },

  closeEdit(e) {
    e.stopPropagation();
    this.$('.edit-wrapper').addClass('hide');
    this.$('.edit-action').addClass('hide');
    this.$('.text-wrapper').removeClass('hide');
    this.$('.edit').removeClass('hide');
    this.$('.delete').removeClass('hide');
  },

  saveEdit(e) {
    e.stopPropagation();
    const _this = this;
    const c_type = this.model.get('type');
    const new_body = this.$('.edit-civi-body')
      .val()
      .trim();
    new_title = this.$('.edit-civi-title')
      .val()
      .trim();
    let links;
    if (c_type != 'response' && c_type != 'rebuttal') {
      links = this.magicSuggestView.ms.getValue();
    } else {
      links = [];
    }

    let new_type = this.$("#civi-type-form input[type='radio']:checked").val();
    console.log(new_type);
    if (!new_body || !new_title) {
      Materialize.toast('Please do not leave fields blank', 5000);
      return;
    } if (
      this.imageRemoveList.length === 0
      && this.attachmentCount === 0
      && (new_body == this.model.get('body')
        && new_title == this.model.get('title')
        && _.isEqual(links, this.model.get('links'))
        && new_type == this.model.get('type'))
    ) {
      this.closeEdit(e);
      return;
    }
    let data;

    if (c_type === 'response' || c_type === 'rebuttal') {
      new_type = c_type;
      data = {
        civi_id: this.model.id,
        title: new_title,
        body: new_body,
      };
    } else {
      data = {
        civi_id: this.model.id,
        title: new_title,
        body: new_body,
        links,
        type: new_type,
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
        _this.closeEdit(e);
        // var score = $this.find('.rate-value');
        // var new_vote = parseInt(score.text())+ 1;
        // score.text(new_vote);
        //
        const attachment_input = _this.$('#id_attachment_image');
        const uploaded_images = attachment_input[0].files;
        if (_this.attachmentCount > 0) {
          const formData = new FormData(_this.$('#attachment_image_form')[0]);
          formData.set('civi_id', _this.model.id);
          if (_this.attachment_links.length) {
            _.each(_this.attachment_links, (img_link) => {
              formData.append('attachment_links[]', img_link);
            });
          }

          $.ajax({
            url: '/api/upload_images/',
            type: 'POST',
            success(response2) {
              Materialize.toast('Saved.', 5000);

              // Set the models with new data and rerender
              _this.model.set('title', new_title);
              _this.model.set('body', new_body);
              _this.model.set('links', links);
              _this.model.set('type', new_type);
              _this.model.set('attachments', response2.attachments);
              _this.model.set('score', response.score);
              if (_this.magicSuggestView) {
                _this.magicSuggestView.remove();
              }

              _this.render();

              if (
                _this.model.get('type') != 'response'
                  && _this.model.get('type') != 'rebuttal'
              ) {
                const parent_links = _this.model.get('links');
                _.each(
                  parent_links,
                  (parent_id) => {
                    const parent_civi = _this.options.parentView.civis.get(parent_id);
                    if (parent_civi) {
                      const prev_links = parent_civi.get('links');
                      prev_links.push(_this.model.id);
                      parent_civi.set('links', prev_links);
                    }
                  },
                  this,
                );

                _this.parentView.initRecommended(); // THISTHIS
                _this.parentView.renderBodyContents();
                _this.parentView.processCiviScroll();
              }
            },
            error(e) {
              Materialize.toast(
                'Civi was edited but one or more images could not be uploaded',
                5000,
              );

              // Set the models with new data and rerender
              _this.model.set('title', new_title);
              _this.model.set('body', new_body);
              _this.model.set('links', links);
              _this.model.set('type', new_type);
              _this.model.set('attachments', response2.attachments);
              _this.model.set('score', response.score);
              if (_this.magicSuggestView) {
                _this.magicSuggestView.remove();
              }

              _this.render();

              if (
                _this.model.get('type') != 'response'
                  && _this.model.get('type') != 'rebuttal'
              ) {
                const parent_links = _this.model.get('links');
                _.each(
                  parent_links,
                  (parent_id) => {
                    const parent_civi = _this.options.parentView.civis.get(parent_id);
                    if (parent_civi) {
                      const prev_links = parent_civi.get('links');
                      prev_links.push(_this.model.id);
                      parent_civi.set('links', prev_links);
                    }
                  },
                  this,
                );

                _this.parentView.initRecommended(); // THISTHIS
                _this.parentView.renderBodyContents();
                _this.parentView.processCiviScroll();
              }
            },
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
          });
        } else {
          Materialize.toast('Saved', 5000);

          // Clean up previous links
          if (_this.model.get('type') != 'response' && _this.model.get('type') != 'rebuttal') {
            const orig_links = _this.model.get('links');
            _.each(
              orig_links,
              (parent_id) => {
                const parent_civi = _this.options.parentView.civis.get(parent_id);
                if (parent_civi) {
                  const prev_links = parent_civi.get('links');
                  const cleaned = _.without(prev_links, _this.model.id);
                  parent_civi.set('links', cleaned);
                }
              },
              this,
            );
          }
          // Set the models with new data and rerender
          _this.model.set('title', new_title);
          _this.model.set('body', new_body);
          _this.model.set('links', links);
          _this.model.set('type', new_type);
          _this.model.set('attachments', response.attachments);
          _this.model.set('score', response.score);
          if (_this.magicSuggestView) {
            _this.magicSuggestView.remove();
          }

          _this.render();

          if (_this.model.get('type') != 'response' && _this.model.get('type') != 'rebuttal') {
            const parent_links = _this.model.get('links');
            _.each(
              parent_links,
              (parent_id) => {
                const parent_civi = _this.options.parentView.civis.get(parent_id);
                if (parent_civi) {
                  const prev_links = parent_civi.get('links');
                  prev_links.push(_this.model.id);
                  parent_civi.set('links', prev_links);
                }
              },
              this,
            );

            _this.parentView.initRecommended(); // THISTHIS
            _this.parentView.renderBodyContents();
            _this.parentView.processCiviScroll();
          }
        }
      },
      error(r) {
        Materialize.toast('Could not edit the civi', 5000);
        _this.closeEdit(e);
        _this.render();
      },
    });
  },

  deleteEdit(e) {
    const _this = this;
    e.stopPropagation();

    $.ajax({
      url: '/api/delete_civi/',
      type: 'POST',
      data: {
        civi_id: this.model.id,
      },
      success(response) {
        Materialize.toast('Deleted Civi succssfully', 5000);
        _.each(_this.model.get('links'), (link) => {
          const linked_civi = _this.civis.findWhere({ id: link });
          const prev_links = linked_civi.get('links');
          new_links = _.without(prev_links, _this.model.id);
          linked_civi.set('links', new_links);
        });

        _this.civis.remove(_this.model);
        _this.remove();
        _this.parentView.initRecommended();
        _this.parentView.renderBodyContents();
        _this.parentView.processCiviScroll();
      },
      error(r) {
        Materialize.toast('Could not delete the civi', 5000);
      },
    });
  },
});

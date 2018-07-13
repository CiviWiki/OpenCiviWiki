import { View } from 'backbone.marionette';

const EditThreadView = View.extend({
  el: '.thread-wiki-holder',
  template: _.template($('#edit-wiki-template').html()),
  initialize(options) {
    this.options = options || {};
    this.threadId = options.threadId;
    this.parentView = options.parentView;
    this.removeImage = false;
    this.imageMode = '';
    this.render();
  },

  render() {
    this.$el.empty().append(this.template());
    this.$('#thread-image-forms').addClass('hide');

    this.$('#thread-location').val(this.model.get('level'));
    if (this.model.get('state')) {
      this.$('.edit-thread-state-selection').removeClass('hide');
      this.$('#thread-state').val(this.model.get('state'));
    }
    // cw.materializeShit();
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

  show() {
    this.$('.edit-thread-modal').openModal();
  },

  hide() {
    this.$('.edit-thread-modal').closeModal();
  },

  showStates() {
    const level = this.$el.find('#thread-location').val();
    if (level === 'state') {
      this.$('.edit-thread-state-selection').removeClass('hide');
    } else {
      this.$('.edit-thread-state-selection').addClass('hide');
      this.$el.find('#thread-state').val('');
    }
  },

  cancelEdit() {
    this.parentView.threadWikiRender();
  },

  showImageForm() {
    this.$('#thread-image-forms').removeClass('hide');
    this.$('.previous-image').addClass('hide');
    this.removeImage = true;
  },

  hideImageForm() {
    this.$('#thread-image-forms').addClass('hide');
    this.$('.previous-image').removeClass('hide');
    this.removeImage = false;
  },
  showImageUploadForm() {
    this.imageMode = 'upload';
    this.$('#attachment_image_form').removeClass('hide');
    this.$('#link-image-form').addClass('hide');
  },
  showImageLinkForm() {
    this.imageMode = 'link';
    this.$('#attachment_image_form').addClass('hide');
    this.$('#link-image-form').removeClass('hide');
  },

  editThread(event) {
    const view = this;
    view
      .$(event.currentTarget)
      .addClass('disabled')
      .attr('disabled', true);
    const title = this.$el
      .find('#thread-title')
      .val()
      .trim();
    const summary = this.$el
      .find('#thread-body')
      .val()
      .trim();
    const level = this.$el.find('#thread-location').val();
    const categoryId = this.$el.find('#thread-category').val();

    let state = '';
    if (level === 'state') {
      state = this.$el.find('#thread-state').val();
    }
    const thread = this.threadId;
    if (title && summary && categoryId) {
      $.ajax({
        url: '/api/edit_thread/',
        type: 'POST',
        data: {
          title,
          summary,
          category_id: categoryId,
          thread_id: thread,
          level,
          state,
        },
        success(response) {
          const file = $('#thread_attachment_image').val();
          const imageUrl = view
            .$('#link-image-form')
            .val()
            .trim();
          if (view.removeImage) {
            // if file
            if (view.imageMode === 'upload' && file) {
              const formData = new FormData(view.$('#attachment_image_form')[0]);
              formData.set('thread_id', response.data.thread_id);
              $.ajax({
                url: '/api/upload_image/',
                type: 'POST',
                success(imageResponse) {
                  M.toast({ html: 'Saved changes' });

                  const newData = response.data;
                  view.parentView.model.set(newData);
                  view.parentView.model.set('image', imageResponse.image);
                  view.parentView.threadWikiRender();
                },
                error(e) {
                  M.toast({ html: 'ERROR: Image could not be uploaded' });
                  M.toast({ html: e.statusText });
                  view
                    .$(event.currentTarget)
                    .removeClass('disabled')
                    .attr('disabled', false);
                },
                data: formData,
                cache: false,
                contentType: false,
                processData: false,
              });
            } else if (view.imageMode === 'link' && imageUrl) {
              $.ajax({
                url: '/api/upload_image/',
                type: 'POST',
                data: {
                  link: imageUrl,
                  thread_id: response.data.thread_id,
                },
                success(imageResponse) {
                  M.toast({ html: 'Saved changes' });
                  view.hide();

                  const newData = response.data;
                  view.parentView.model.set(newData);
                  view.parentView.model.set('image', imageResponse.image);
                  view.parentView.threadWikiRender();
                },
                error(error) {
                  M.toast({ html: 'ERROR: Image could not be uploaded' });
                  M.toast({ html: error.statusText });
                  view
                    .$(event.currentTarget)
                    .removeClass('disabled')
                    .attr('disabled', false);
                },
              });
            } else {
              // Remove image
              $.ajax({
                url: '/api/upload_image/',
                type: 'POST',
                data: {
                  remove: true,
                  thread_id: response.data.thread_id,
                },
                success() {
                  M.toast({ html: 'Saved changes' });
                  // view.hide();

                  const newData = response.data;
                  view.parentView.model.set(newData);
                  view.parentView.threadWikiRender();
                },
                error(error) {
                  M.toast({ html: 'ERROR: Image could not be uploaded' });
                  M.toast({ html: error.statusText });
                  view
                    .$(event.currentTarget)
                    .removeClass('disabled')
                    .attr('disabled', false);
                },
              });
            }
          } else {
            M.toast({ html: 'Saved changes' });
            // view.hide();

            // New Data
            const newData = response.data;
            view.parentView.model.set(newData);
            view.parentView.threadWikiRender();
          }
        },
        error() {
          M.toast({ html: 'Servor Error: Thread could not be edited' });
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
export default EditThreadView;

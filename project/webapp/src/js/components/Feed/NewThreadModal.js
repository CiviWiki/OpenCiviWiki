import { View } from 'backbone.marionette';
import modalTemplate from 'Templates/components/Feed/new_thread.html';
import STATES from '../../utils/states';

const NewThreadModal = View.extend({
  template: modalTemplate,

  ui: {
    newThreadModal: '.new-thread-modal',
  },

  initialize(options) {
    this.categories = options.categories.models;
    this.templateContext = {
      states: STATES,
      categories: options.categories.toJSON(),
    };
    this.imageMode = '';
  },

  onRender() {
    M.AutoInit();
    M.Modal.init(this.getUI('newThreadModal'));
    this.modal = M.Modal.getInstance(this.getUI('newThreadModal'));
  },

  openModal() {
    this.modal.open();
  },

  closeModal() {
    this.modal.close();
  },

  events: {
    'click .cancel-new-thread': 'cancelThread',
    'click .draft-new-thread': 'draftThread',
    'click #image-from-computer': 'showImageUploadForm',
    'click #image-from-link': 'showImageLinkForm',
    'change #thread-location': 'showStates',
  },

  cancelThread() {
    this.closeModal();
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
  showStates() {
    const level = this.$el.find('#thread-location').val();
    if (level === 'state') {
      this.$('.new-thread-state-selection').removeClass('hide');
    } else {
      this.$('.new-thread-state-selection').addClass('hide');
    }
  },

  draftThread() {
    const view = this;
    const formTitle = this.$el.find('#thread-title').val();
    const formSummary = this.$el.find('#thread-body').val();
    const formLevel = this.$el.find('#thread-location').val();
    const formCategoryId = this.$el.find('#thread-category').val();

    let formState = '';
    if (formLevel === 'state') {
      formState = this.$el.find('#thread-state').val();
    }
    if (formTitle && formSummary && formCategoryId) {
      $.ajax({
        url: '/api/new_thread/',
        type: 'POST',
        data: {
          title: formTitle,
          summary: formSummary,
          category_id: formCategoryId,
          level: formLevel,
          state: formState,
          is_draft: 'True',
        },
        success(response) {
          if (view.imageMode === 'upload') {
            const file = $('#id_attachment_image').val();

            if (file) {
              const formData = new FormData(view.$('#attachment_image_form')[0]);
              formData.set('thread_id', response.thread_id);
              $.ajax({
                url: '/api/upload_image/',
                type: 'POST',
                success() {
                  M.toast({ html: 'New thread created.' });
                  window.location = `thread/${response.thread_id}`;
                },
                error(e) {
                  M.toast({ html: 'ERROR: Image could not be uploaded' });
                  M.toast({ html: e.statusText });
                },
                data: formData,
                cache: false,
                contentType: false,
                processData: false,
              });
            }
          } else if (view.imageMode === 'link') {
            const imageUrl = view
              .$('#link-image-form')
              .val()
              .trim();
            if (imageUrl) {
              $.ajax({
                url: '/api/upload_image/',
                type: 'POST',
                data: {
                  link: imageUrl,
                  thread_id: response.thread_id,
                },
                success() {
                  M.toast({ html: 'New thread created.' });
                  window.location = `thread/${response.thread_id}`;
                },
                error(e) {
                  M.toast({ html: 'ERROR: Image could not be uploaded' });
                  M.toast({ html: e.statusText });
                },
              });
            }
          } else {
            M.toast({ html: 'New thread created.' });
            window.location = `thread/${response.thread_id}`;
          }
        },
        error(e) {
          M.toast({ html: 'ERROR: Thread could not be created' });
          M.toast({ html: e.statusText });
        },
      });
    } else {
      M.toast({ html: 'Please input all fields.' });
    }
  },
});

export default NewThreadModal;

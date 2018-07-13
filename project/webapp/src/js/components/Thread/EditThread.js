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
    cw.materializeShit();
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

  editThread(e) {
    const _this = this;
    _this
      .$(e.currentTarget)
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


    const category_id = this.$el.find('#thread-category').val();


    let state = '';
    if (level === 'state') {
      state = this.$el.find('#thread-state').val();
    }
    const thread_id = this.threadId;
    console.log(title, summary, category_id, thread_id);
    if (title && summary && category_id) {
      $.ajax({
        url: '/api/edit_thread/',
        type: 'POST',
        data: {
          title,
          summary,
          category_id,
          thread_id,
          level,
          state,
        },
        success(response) {
          const file = $('#thread_attachment_image').val();
          const img_url = _this
            .$('#link-image-form')
            .val()
            .trim();
          if (_this.removeImage) {
            // if file
            if (_this.imageMode === 'upload' && file) {
              const formData = new FormData(_this.$('#attachment_image_form')[0]);
              formData.set('thread_id', response.data.thread_id);
              $.ajax({
                url: '/api/upload_image/',
                type: 'POST',
                success(response2) {
                  Materialize.toast('Saved changes', 5000);
                  // _this.hide();

                  new_data = response.data;
                  _this.parentView.model.set('title', new_data.title);
                  _this.parentView.model.set('summary', new_data.summary);
                  _this.parentView.model.set('category', new_data.category);
                  _this.parentView.model.set('level', new_data.level);
                  _this.parentView.model.set('state', new_data.state);
                  _this.parentView.model.set('location', new_data.location);
                  _this.parentView.model.set('image', response2.image);
                  _this.parentView.threadWikiRender();
                },
                error(e) {
                  Materialize.toast('ERROR: Image could not be uploaded', 5000);
                  Materialize.toast(e.statusText, 5000);
                  _this
                    .$(e.currentTarget)
                    .removeClass('disabled')
                    .attr('disabled', false);
                },
                data: formData,
                cache: false,
                contentType: false,
                processData: false,
              });
            } else if (_this.imageMode === 'link' && img_url) {
              $.ajax({
                url: '/api/upload_image/',
                type: 'POST',
                data: {
                  link: img_url,
                  thread_id: response.data.thread_id,
                },
                success(response2) {
                  Materialize.toast('Saved changes', 5000);
                  _this.hide();

                  new_data = response.data;
                  _this.parentView.model.set('title', new_data.title);
                  _this.parentView.model.set('summary', new_data.summary);
                  _this.parentView.model.set('category', new_data.category);
                  _this.parentView.model.set('level', new_data.level);
                  _this.parentView.model.set('state', new_data.state);
                  _this.parentView.model.set('location', new_data.location);
                  _this.parentView.model.set('image', response2.image);
                  _this.parentView.threadWikiRender();
                },
                error(e) {
                  Materialize.toast('ERROR: Image could not be uploaded', 5000);
                  Materialize.toast(e.statusText, 5000);
                  _this
                    .$(e.currentTarget)
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
                success(response2) {
                  Materialize.toast('Saved changes', 5000);
                  // _this.hide();

                  new_data = response.data;
                  _this.parentView.model.set('title', new_data.title);
                  _this.parentView.model.set('summary', new_data.summary);
                  _this.parentView.model.set('category', new_data.category);
                  _this.parentView.model.set('image', response2.image);
                  _this.parentView.model.set('level', new_data.level);
                  _this.parentView.model.set('state', new_data.state);
                  _this.parentView.model.set('location', new_data.location);
                  _this.parentView.threadWikiRender();
                },
                error(e) {
                  Materialize.toast('ERROR: Image could not be uploaded', 5000);
                  Materialize.toast(e.statusText, 5000);
                  _this
                    .$(e.currentTarget)
                    .removeClass('disabled')
                    .attr('disabled', false);
                },
              });
            }
          } else {
            Materialize.toast('Saved changes', 5000);
            // _this.hide();

            // New Data
            new_data = response.data;
            _this.parentView.model.set('title', new_data.title);
            _this.parentView.model.set('summary', new_data.summary);
            _this.parentView.model.set('category', new_data.category);
            _this.parentView.model.set('level', new_data.level);
            _this.parentView.model.set('state', new_data.state);
            _this.parentView.model.set('location', new_data.location);
            _this.parentView.threadWikiRender();
          }
        },
        error() {
          Materialize.toast('Servor Error: Thread could not be edited', 5000);
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
export default EditThreadView;

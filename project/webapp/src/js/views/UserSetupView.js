import { View } from 'backbone.marionette';

import baseTemplate from 'Templates/layouts/user_setup.html';
import step0Template from 'Templates/components/UserSetup/step0.html';
import step1Template from 'Templates/components/UserSetup/step1.html';
import step2Template from 'Templates/components/UserSetup/step2.html';
import step3Template from 'Templates/components/UserSetup/step3.html';
import MapView from '../components/Map/MapView';
import { GoogleMap } from '../models';

import 'Styles/setup.less';

const UserSetupView = View.extend({
  id: 'user-setup',
  template: baseTemplate,

  step0Template,
  step1Template,
  step2Template,
  step3Template,

  regions: {
    step0: '#step0',
    step1: '#step1',
    step2: '#step2',
    step3: '#step3',
  },

  initialize() {
    this.currentStep = 0;
    this.googleAPIKey = this.getOption('context').GoogleAPIKey;
    this.mapView = new MapView({ model: new GoogleMap(), googleMapsApiKey: this.googleAPIKey });

    this.listenTo(this.model, 'sync', this.renderView);
  },

  renderView() {
    if (this.currentStep === 0) {
      this.$('#step0')
        .empty()
        .append(this.step0Template());
      this.$('#step1')
        .empty()
        .append(this.step1Template({ username: this.model.id }))
        .toggleClass('hide');
      this.$('#step2')
        .empty()
        .append(this.step2Template())
        .toggleClass('hide');
      this.$('#step3')
        .empty()
        .append(this.step3Template())
        .toggleClass('hide');

      M.updateTextFields();
      // Init map view for locating the user
      this.mapView.renderAndInitMap();
      this.listenTo(this.mapView.model, 'change', _.bind(this.validateStep2, this));
    }
  },

  events: {
    'click .prev': 'prevStep',
    'click .next': 'nextStep',
    'click .finish': 'setupUser',
    'change .profile-image-pick': 'previewImage',
    'click .cancel-image': 'clearImageField',
    'click .upload-image': 'toggleFileDialog',
    'keypress .about-me': 'limitInput',
    'input .step1-input': 'validateStep1',
  },

  nextStep() {
    if (this.currentStep === 0) {
      this.$('#step0').addClass('hide');
      this.$('#step1').removeClass('hide');
      this.currentStep = 1;
    } else if (this.currentStep === 1) {
      const firstName = this.$el.find('#first-name').val();

      const lastName = this.$el.find('#last-name').val();

      const aboutMe = this.$el.find('#about-me').val();

      if (firstName && lastName && aboutMe) {
        this.$el.find('#step1').addClass('hide');
        this.$el.find('#step2').removeClass('hide');
        this.mapView.resizeMap().adjustMapCenter();
        this.currentStep = 2;
      } else {
        M.toast({ html: 'Please fill out all the fields' });
      }
    } else if (this.currentStep === 2) {
      this.$('#step2').addClass('hide');
      this.$('#step3').removeClass('hide');
    }
  },

  prevStep() {
    if (this.currentStep === 2) {
      this.$el.find('#step1').removeClass('hide');
      this.$el.find('#step2').addClass('hide');
      this.currentStep = 1;
    }
  },

  // INPUT VALIDATION ============================================================
  // limitInput(): limits the about-me input field  to 500 characters
  limitInput(event) {
    const max = 500;
    const textarea = this.$el.find('#about-me');
    if (event.which < 0x20) {
      return;
    }
    if (textarea.val().length === max) {
      event.preventDefault();
    } else if (textarea.val().length > max) {
      textarea.val(textarea.val().substring(0, max));
    }
  },

  validateStep1() {
    const firstName = this.$el
      .find('#first-name')
      .val()
      .trim();

    const lastName = this.$el
      .find('#last-name')
      .val()
      .trim();

    const aboutMe = this.$el
      .find('#about-me')
      .val()
      .trim();

    if (firstName && lastName && aboutMe) {
      this.model.set({
        first_name: firstName,
        last_name: lastName,
        about_me: aboutMe,
      });

      this.$el.find('.next').removeClass('disabled');
      this.$el.find('.help-text.invalid').addClass('hide');
      this.$el.find('.help-text.valid').removeClass('hide');
    } else {
      this.$el.find('.next').addClass('disabled');
      this.$el.find('.help-text.valid').addClass('hide');
      this.$el.find('.help-text.invalid').removeClass('hide');
    }
  },

  validateStep2() {
    const coordinates = this.mapView.model.get('coordinates');

    const address = this.mapView.model.get('address');

    if (_.isEmpty(coordinates) || _.isEmpty(address)) {
      this.$el
        .find('.finish')
        .addClass('disabled')
        .attr('disabled', true);
    } else {
      this.model.set({
        longitude: coordinates.lng,
        latitude: coordinates.lat,
        address: address.address,
        city: address.city,
        state: address.state,
        zip_code: address.zipcode,
      });

      this.$el
        .find('.finish')
        .removeClass('disabled')
        .attr('disabled', false);
    }
  },

  // IMAGE SELECTION & PREVIEW ===================================================
  /**
   * displays the appropriate buttons based on image state
   */
  toggleImgButtons() {
    this.$el.find('.profile-image-pick').toggleClass('hide');
    this.$el.find('.upload-image').toggleClass('hide');
    this.$el.find('.cancel-image').toggleClass('hide');
    this.$el.find('.preview-image').toggleClass('hide');
  },

  /**
   * Lets the user choose a different image
   * @param {Event} event
   */
  toggleFileDialog(event) {
    event.stopPropagation();
    event.preventDefault();
    this.$el.find('#id_profile_image').trigger('click');
  },

  /**
   * Creates a preview of the current image file chosen
   */
  previewImage() {
    const img = this.$el.find('#id_profile_image');
    if (img.val()) {
      this.uploadProfileImg();
    }
  },

  /**
   * clears only the profile image file field
   * @param {Event} event
   */
  clearImageField(event) {
    this.clearProfileImg();

    event.stopPropagation();
    event.preventDefault();
  },

  // SENDING REQUEST TO SERVER ===================================================
  setupUser() {
    const view = this;
    this.model.save(
      {},
      {
        type: 'PATCH',
        success() {
          M.toast({ html: 'Success' });
          view.nextStep();
        },
        error(data) {
          if (data.status_code === 400) {
            M.toast({ html: data.message });
          } else if (data.status_code === 500) {
            M.toast({ html: 'Internal Server Error' });
          } else {
            _.each(data, (message, type) => {
              M.toast({ html: `${type}: ${message}[0]` });
            });
          }
        },
      },
    );
  },

  uploadProfileImg() {
    const view = this;
    const formData = new FormData(this.$el.find('#profile_image_form')[0]);

    $.ajax({
      url: '/api/upload_profile/',
      type: 'POST',
      success(response) {
        const img = view.$el.find('#id_profile_image');
        const uploadedImage = img[0].files[0];
        if (uploadedImage) {
          const previewImage = view.$el.find('.preview-image');
          previewImage.attr('src', response.profile_image);

          if (view.$el.find('.preview-image').hasClass('hide')) {
            view.toggleImgButtons();
            view.$el.find('.loading').addClass('hide');
            view.$el.find('.placeholder').addClass('hide');
          }
        }

        M.toast({ html: 'Image Uploaded!' });
      },
      error(response) {
        if (response.status === 400) {
          M.toast({ html: response.responseJSON.message, classes: 'red' });
        } else if (response.status === 500) {
          M.toast({ html: 'Internal Server Error', classes: 'red' });
        } else {
          M.toast({ html: response.statusText, classes: 'red' });
        }

        view.$el.find('.loading').addClass('hide');
        view.$el.find('.placeholder').removeClass('hide');
        view.$el.find('#profile_image_form')[0].reset();
      },
      data: formData,
      cache: false,
      contentType: false,
      processData: false,
    });
    this.$el.find('.loading').removeClass('hide');
    this.$el.find('.placeholder').addClass('hide');
    return false;
  },

  clearProfileImg() {
    const view = this;
    $.ajax({
      url: '/api/clear_profile/',
      type: 'POST',
      success(response) {
        view.toggleImgButtons();
        view.$el.find('.loading').addClass('hide');
        view.$el.find('.placeholder').removeClass('hide');
        view.$el.find('#profile_image_form')[0].reset();
        M.toast({ html: JSON.stringify(response) });
      },
      error(response) {
        M.toast({ html: JSON.stringify(response) });
      },
    });
  },
});

export default UserSetupView;

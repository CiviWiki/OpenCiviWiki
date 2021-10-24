cw = cw || {};

cw.AccountModel = BB.Model.extend({
  defaults: function() {
    return {
      username: "",
      first_name: "",
      last_name: "",
      about_me: ""
    };
  },
  urlRoot: "/api/v1/accounts/",

  idAttribute: "username",
  initialize: function(model, options) {
    options = options || {};
  }
});

cw.UserSetupView = BB.View.extend({
  el: "#user-setup",

  currentStep: 0,
  baseTemplate: _.template($("#setup-base-template").html()),
  step0Template: _.template($("#step0-template").html()),
  step1Template: _.template($("#step1-template").html()),
  step2Template: _.template($("#step2-template").html()),

  initialize: function(options) {
    options = options || {};

    this.listenTo(this.model, "sync", this.render);
    return this;
  },

  render: function() {
    if (this.currentStep === 0) {
      this.$el.empty().append(this.baseTemplate());
      this.$("#step0")
        .empty()
        .append(this.step0Template());
      this.$("#step1")
        .empty()
        .append(this.step1Template())
        .toggleClass("hide");
      this.$("#step2")
        .empty()
        .append(this.step2Template())
        .toggleClass("hide");
    }
  },

  events: {
    "click .prev": "prevStep",
    "click .next": "nextStep",
    "click .finish": "setupUser",
    "change .profile-image-pick": "previewImage",
    "click .cancel-image": "clearImageField",
    "click .upload-image": "toggleFileDialog",
    "keypress .about-me": "limitInput",
    "input .step1-input": "validateStep1"
  },

  nextStep: function() {
    if (this.currentStep === 0) {
      this.$("#step0").addClass("hide");
      this.$("#step1").removeClass("hide");
      this.currentStep = 1;
    } else if (this.currentStep === 1) {
      var first_name = this.$el.find("#first-name").val();
      var last_name = this.$el.find("#last-name").val();
      var about_me = this.$el.find("#about-me").val();

      if (first_name && last_name && about_me) {
        this.$el.find("#step1").addClass("hide");
        this.$el.find("#step2").removeClass("hide");
        this.currentStep = 2;
      } else {
        Materialize.toast(
          '<span class="subtitle-lato white-text">Please fill out all the fields</span>',
          5000
        );
      }
    }
  },

  prevStep: function() {
    if (this.currentStep === 2) {
      this.$el.find("#step1").removeClass("hide");
      this.$el.find("#step2").addClass("hide");
      this.currentStep = 1;
    }
  },

  // INPUT VALIDATION ============================================================
  // limitInput(): limits the about-me input field  to 500 characters
  limitInput: function(e) {
    var max = 500;
    var textarea = this.$el.find("#about-me");
    if (e.which < 0x20) {
      return;
    }
    if (textarea.val().length == max) {
      e.preventDefault();
    } else if (textarea.val().length > max) {
      textarea.val(textarea.val().substring(0, max));
    }
  },

  validateStep1: function() {
    var first_name = this.$el
      .find("#first-name")
      .val()
      .trim();

    var last_name = this.$el
      .find("#last-name")
      .val()
      .trim();

    var about_me = this.$el
      .find("#about-me")
      .val()
      .trim();

    if (first_name && last_name && about_me) {
      this.model.set({
        first_name: first_name,
        last_name: last_name,
        about_me: about_me
      });

      this.$el.find(".finish").removeClass("disabled");
      this.$el.find(".help-text.invalid").addClass("hide");
      this.$el.find(".help-text.valid").removeClass("hide");
    } else {
      this.$el.find(".finish").addClass("disabled");
      this.$el.find(".help-text.valid").addClass("hide");
      this.$el.find(".help-text.invalid").removeClass("hide");
    }
  },

  // IMAGE SELECTION & PREVIEW ===================================================
  // toggleImgButtons(): displays the appropriate buttons based on image state
  toggleImgButtons: function() {
    this.$el.find(".profile-image-pick").toggleClass("hide");
    this.$el.find(".upload-image").toggleClass("hide");
    this.$el.find(".cancel-image").toggleClass("hide");
    this.$el.find(".preview-image").toggleClass("hide");
  },

  // toggleFileDialog(): Lets the user choose a different image
  toggleFileDialog: function(e) {
    e.stopPropagation();
    e.preventDefault();
    this.$el.find("#id_profile_image").trigger("click");
  },

  // previewImage(): Creates a preview of the current image file chosen
  previewImage: function(e) {
    var _this = this;
    var img = this.$el.find("#id_profile_image");
    if (img.val()) {
      this.uploadProfileImg();
    }
  },

  // clearImageField(): clears only the profile image file field
  clearImageField: function(e) {
    this.clearProfileImg();

    e.stopPropagation();
    e.preventDefault();
  },

  // SENDING REQUEST TO SERVER ===================================================
  setupUser: function() {
    // preserve reference to 'this' for use in ajax callback
    var _this = this;

    var first_name = this.model.get("first_name");
    var last_name = this.model.get("last_name");
    var about_me = this.model.get("about_me");

    if (first_name && last_name && about_me) {
      var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

      $.ajax({
        type: "POST",
        url: "/api/edituser/",
        data: {
          csrfmiddlewaretoken: csrftoken,
          full_profile: "True",
          about_me: about_me,
          first_name: first_name,
          last_name: last_name,
        },
        success: function(data) {
          Materialize.toast(
            '<span class="subtitle-lato white-text">Success</span>',
            5000
          );
          _this.nextStep();
        },
        error: function(data) {
          Materialize.toast(data.statusText, 5000);
        }
      });
    }
  },

  uploadProfileImg: function() {
    var _this = this;
    var formData = new FormData(this.$el.find("#profile_image_form")[0]);

    $.ajax({
      url: "/api/upload_profile/",
      type: "POST",
      success: function(response) {
        var img = _this.$el.find("#id_profile_image");
        var uploaded_image = img[0].files[0];
        if (uploaded_image) {
          var preview_image = _this.$el.find(".preview-image");
          preview_image.attr("src", response.profile_image);

          if (_this.$el.find(".preview-image").hasClass("hide")) {
            _this.toggleImgButtons();
            _this.$el.find(".loading").addClass("hide");
            _this.$el.find(".placeholder").addClass("hide");
          }
        }

        Materialize.toast("Image Uploaded!", 5000);
      },
      error: function(response) {
        if (response.status === 400) {
          Materialize.toast(response.responseJSON.message, 5000, "red");
        } else if (response.status === 500) {
          Materialize.toast("Internal Server Error", 5000, "red");
        } else {
          Materialize.toast(response.statusText, 5000, "red");
        }

        _this.$el.find(".loading").addClass("hide");
        _this.$el.find(".placeholder").removeClass("hide");
        _this.$el.find("#profile_image_form")[0].reset();
      },
      data: formData,
      cache: false,
      contentType: false,
      processData: false
    });
    this.$el.find(".loading").removeClass("hide");
    this.$el.find(".placeholder").addClass("hide");
    return false;
  },

  clearProfileImg: function() {
    var _this = this;
    $.ajax({
      url: "/api/clear_profile/",
      type: "POST",
      success: function(e) {
        _this.toggleImgButtons();
        _this.$el.find(".loading").addClass("hide");
        _this.$el.find(".placeholder").removeClass("hide");
        _this.$el.find("#profile_image_form")[0].reset();
        Materialize.toast(JSON.stringify(e), 5000);
      },
      error: function(e) {
        Materialize.toast(JSON.stringify(e), 5000);
      }
    });
  }
});

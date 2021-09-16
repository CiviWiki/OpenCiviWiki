from django import forms
from django.core.files.images import get_image_dimensions
from django.contrib.auth import get_user_model
from accounts.models import Profile


class UpdatePassword(forms.ModelForm):
    """
    Form for updating User Password
    """

    class Meta:
        model = get_user_model()
        fields = ["password", "verify"]

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
                "required": "True",
            }
        ),
    )
    verify = forms.CharField(
        label="Password Verify",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password Verify",
                "required": "True",
            }
        ),
        help_text="Please retype your password.",
    )

    def clean(self):
        """
        Verifies that the passwords match
        """
        clean_data = super(UpdatePassword, self).clean()
        if "password" in clean_data and "verify" in clean_data:
            if clean_data["password"] != clean_data["verify"]:
                raise forms.ValidationError("Passwords don't match.")
        else:
            raise forms.ValidationError("Both password fields need to be filled out.")
        return clean_data


class UpdateProfileImage(forms.ModelForm):
    """
    Form for updating profile image
    """

    class Meta:
        model = Profile
        fields = ["profile_image"]

    profile_image = forms.ImageField()

    def clean_profile_image(self):
        """
        This function is used to make sure that profile images follow Civiwiki standards.

        Requirements:
            - Height cannot exceed 960px
            - Width cannot exceed 1280px
            - Image must be (jpg, jpeg, pjeg, png)
            - File size cannot exceed 2MB
        """
        profile_image = self.cleaned_data["profile_image"]

        try:
            w, h = get_image_dimensions(profile_image)

            # validate dimensions
            max_height = 960
            max_width = 1280
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u"Please use an image that is {w} x {h} pixels or smaller.".format(
                        w=max_width, h=max_height
                    )
                )

            # validate content type
            main, sub = profile_image.content_type.split("/")
            if not (main == "image" and sub in ["jpg", "jpeg", "pjpeg", "png"]):
                raise forms.ValidationError(u"Please use a JPEG or PNG image.")

            # validate file size
            if len(profile_image) > (2000 * 1024):
                raise forms.ValidationError(
                    "Profile image file size may not exceed 2MB."
                )

        except AttributeError:
            pass

        return profile_image

import re
from django.core.files.images import get_image_dimensions
from django import forms
from django.forms.models import ModelForm
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from .reserved_usernames import RESERVED_USERNAMES
from accounts.models import Profile


class UserRegistrationForm(ModelForm):
    """
    This class is used to register a new user in Civiwiki

    Components:
        - Email     - from registration form
        - Username  - from registration form
        - Password  - from registration form
        - Error_Message
            - Invalid_Username - Usernames may only use lowercase characters or numbers
            - Email_Exists - An account exists for this email address
            - Invalid_Password - Password can not be entirely numeric
            - Invalid_Password_Length - Password must be at least 4 characters
    """

    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

    error_message = {
        "invalid_username": _(
            "Usernames may only use lowercase characters or numbers."
        ),
        "email_exists": _("An account exists for this email address."),
        "username_exists": _("Sorry, this username already exists."),
        "invalid_password": _("Password can not be entirely numeric."),
        "invalid_password_length": _("Password must be at least 4 characters."),
    }

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password")

    def clean_email(self):
        """
        Used to make sure user entered email address is a valid email address

        Returns email
        """

        email = self.cleaned_data.get("email")

        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(self.error_message["email_exists"])

        return email

    def clean_username(self):
        """
        Used to make sure that usernames meet the Civiwiki standards

        Requirements:
            - Username can only be made of lower case alphanumeric values
            - Username cannot match entries from RESERVED_USERNAMES

        Returns username
        """

        username = self.cleaned_data.get("username")

        if not re.match(r"^[0-9a-z]*$", username):
            raise forms.ValidationError(self.error_message["invalid_username"])

        if (
            get_user_model().objects.filter(username=username).exists()
            or username in RESERVED_USERNAMES
        ):
            raise forms.ValidationError(self.error_message["username_exists"])

        return username

    def clean_password(self):
        """
        Used to make sure that passwords meet the Civiwiki standards

        Requirements:
            - At least 4 characters in length
            - Cannot be all numbers

        Returns password
        """

        password = self.cleaned_data.get("password")

        if len(password) < 4:
            raise forms.ValidationError(self.error_message["invalid_password_length"])

        if password.isdigit():
            raise forms.ValidationError(self.error_message["invalid_password"])

        return password


class ProfileEditForm(forms.ModelForm):
    """
    Form for updating Profile data
    """

    def __init__(self, *args, **kwargs):
        readonly = kwargs.pop("readonly", False)
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        if readonly:
            self.disable_fields()

    def disable_fields(self):
        for key, value in self.fields.items():
            value.disabled = True

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "about_me",
            "profile_image",
            "username",
            "email",
        ]

    first_name = forms.CharField(label="First Name", max_length=63, required=False)
    last_name = forms.CharField(label="Last Name", max_length=63, required=False)
    about_me = forms.CharField(label="About Me", max_length=511, required=False)
    email = forms.EmailField(label="Email", disabled=True)
    username = forms.CharField(label="Username", disabled=True)
    profile_image = forms.ImageField(required=False)


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
        This function is used to make sure that profile images
        follow Civiwiki standards.

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

import re
from django.core.files.images import get_image_dimensions
from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    SetPasswordForm,
    PasswordResetForm as AuthRecoverUserForm,
)
from django.forms.models import ModelForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from accounts.utils import send_email
from .reserved_usernames import RESERVED_USERNAMES
from accounts.models import Account

User = get_user_model()


class AccountRegistrationForm(ModelForm):
    """
    This class is used to register new account in Civiwiki

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
        model = User
        fields = ("username", "email", "password")

    def clean_email(self):
        """
        Used to make sure user entered email address is a valid email address

        Returns email
        """

        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
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
            User.objects.filter(username=username).exists()
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


class PasswordResetForm(SetPasswordForm):
    """
    A form that lets a user reset their password
    """

    error_messages = dict(
        SetPasswordForm.error_messages,
        **{
            "invalid_password": _("Password can not be entirely numeric."),
            "invalid_password_length": _("Password must be at least 4 characters."),
        }
    )

    def clean_new_password1(self):
        """
        Used to make sure that new passwords meet the Civiwiki standards

        Must be:
            - At least 4 characters in length
            - Cannot be all numbers

        Returns new password
        """

        password = self.cleaned_data.get("new_password1")

        if len(password) < 4:
            raise forms.ValidationError(self.error_messages["invalid_password_length"])

        if password.isdigit():
            raise forms.ValidationError(self.error_messages["invalid_password"])

        return password


class RecoverUserForm(AuthRecoverUserForm):
    """
    Send custom recovery mail with a task runner mostly taken from PasswordResetForm in auth
    """

    def save(
        self,
        domain_override=None,
        subject_template_name=None,
        email_template_name=None,
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
        html_email_template_name=None,
        extra_email_context=None,
    ):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        email = self.cleaned_data["email"]

        for user in self.get_users(email):
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            domain = get_current_site(request).domain
            base_url = "http://{domain}/auth/password_reset/{uid}/{token}/"
            url_with_code = base_url.format(domain=domain, uid=uid, token=token)
            body_txt = """You're receiving this email because you requested an account recovery
                          email for your user account at {domain}. Your username for this email
                          is: {username}. If you also need to reset your password, please go to
                          the following page and choose a new password."""

            email_body = body_txt.format(domain=domain, username=user.username)

            context = {
                "title": "Account Recovery for CiviWiki",
                "greeting": "Recover your account on CiviWiki",
                "body": email_body,
                "link": url_with_code,
            }

            text_message_template = "email/base_text_template.txt"
            html_message_template = "email/base_email_template.html"

            message = render_to_string(text_message_template, context)
            html_message = render_to_string(html_message_template, context)
            sender = settings.EMAIL_HOST_USER
            send_email(
                subject="Account Recovery for CiviWiki",
                message=message,
                sender=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                html_message=html_message,
            )


class UpdateAccount(forms.ModelForm):
    """
    Form for updating Account data
    """

    def __init__(self, *args, **kwargs):
        readonly = kwargs.pop("readonly", False)
        super(UpdateAccount, self).__init__(*args, **kwargs)
        if readonly:
            self.disable_fields()

    def disable_fields(self):
        for _, field in self.fields.items():
            field.disabled = True

    class Meta:
        model = Account
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


User = get_user_model()


class UpdatePassword(forms.ModelForm):
    """
    Form for updating User Password
    """

    class Meta:
        model = User
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
        model = Account
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

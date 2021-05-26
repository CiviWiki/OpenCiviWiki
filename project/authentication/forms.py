import re

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    UserCreationForm,
    SetPasswordForm,
    PasswordResetForm as AuthRecoverUserForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _

from api.tasks import send_email as task_send_email
from .reserved_usernames import RESERVED_USERNAMES


class AccountRegistrationForm(UserCreationForm):
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
    password = forms.CharField(required=True)

    error_message = {
        "invalid_username": _(
            "Usernames may only use lowercase characters or numbers."
        ),
        "email_exists": _("An account exists for this email address."),
        "username_exists": _("Sorry, this username already exists."),
        "invalid_password": _("Password can not be entirely numeric."),
        "invalid_password_length": _("Password must be at least 4 characters."),
    }

    def __init__(self, *args, **kargs):
        super(AccountRegistrationForm, self).__init__(*args, **kargs)
        self.fields["password1"].required = False
        self.fields["password2"].required = False

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

        Retruns username
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

        Retruns password
        """
        password = self.cleaned_data.get("password")

        if len(password) < 4:
            raise forms.ValidationError(self.error_message["invalid_password_length"])

        if password.isdigit():
            raise forms.ValidationError(self.error_message["invalid_password"])

        return password

    def save(self, commit=True):
        """ Saves new users to Civiwiki """
        user = super(AccountRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user


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

        Retruns new password
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
        subject_template_name="email/base_text_template.txt",
        email_template_name="email/base_email_template.html",
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
            email_body = "You're receiving this email because you requested an account recovery email for your user account at {domain}. Your username for this email is: {username}. If you also need to reset your password, please go to the following page and choose a new password.".format(
                domain=domain, username=user.username
            )

            email_context = {
                "title": "Account Recovery for CiviWiki",
                "greeting": "Recover your account on CiviWiki",
                "body": email_body,
                "link": url_with_code,
            }

            task_send_email.delay(
                subject="Account Recovery for CiviWiki",
                recipient_list=[email],
                context=email_context,
            )

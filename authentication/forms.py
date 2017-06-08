from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _
from api.models import Account
from reserved_usernames import RESERVED_USERNAMES
import re

class AccountRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

    error_message = {
        'invalid_username': _("You may only use lowercase characters or numbers and up to one dash."),
        'email_exists': _("An account exists for this email address."),
        'username_exists': _("Sorry, this username is taken."),
        'invalid_password': _("Password can't be entirely numeric."),
        'invalid_password_length': _("Password must be at least 4 characters.")
    }

    def __init__(self, *args, **kargs):
        super(AccountRegistrationForm, self).__init__(*args, **kargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(self.error_message['email_exists'])

        return email


    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not re.match(r'^[0-9a-z]*$', username):
            raise forms.ValidationError(self.error_message['invalid_username'])

        if User.objects.filter(username=username).exists() or username in RESERVED_USERNAMES:
            raise forms.ValidationError(self.error_message['username_exists'])

        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 4:
            raise forms.ValidationError(self.error_message['invalid_password_length'])

        if password.isdigit():
            raise forms.ValidationError(self.error_message['invalid_password'])

        return password


    def save(self, commit=True):
        user = super(AccountRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _
from api.models import Account

class AccountRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=False)
    password = forms.CharField(required=False)

    error_messages = {
        'invalid_username': _("Please Note that both fields may be case-sensitive."),
        'invalid_username_length': _("Please Note that both fields may be case-sensitive."),
        'inactive': _("This account is inactive."),
    }

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def save(self, commit=True):
        user = super(AccountRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        account.beta_access = True

        if commit:
            user.save()

        return user

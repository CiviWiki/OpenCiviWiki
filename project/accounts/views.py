"""
Class based views.

This module will include views for the accounts app.
"""

from django.conf import settings
from django.views.generic.edit import FormView
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import int_to_base36
from django.utils.crypto import salted_hmac
from django.utils.http import urlsafe_base64_encode

from api.models.account import Account
from api.tasks import send_email

from .forms import AccountRegistrationForm
from .models import User
from .authentication import send_activation_email


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """Token Generator for Email Confirmation"""

    key_salt = "django.contrib.auth.tokens.PasswordResetTokenGenerator"

    def _make_token_with_timestamp(self, user, timestamp):
        """ Token function pulled from Django 1.11 """
        ts_b36 = int_to_base36(timestamp)

        hash = salted_hmac(
            self.key_salt, str(user.pk) + str(timestamp)
        ).hexdigest()[::2]
        return "%s-%s" % (ts_b36, hash)


class RegisterView(FormView):
    """
    A form view that handles user registration.
    """
    template_name = 'accounts/register/register.html'
    form_class = AccountRegistrationForm
    success_url = '/'

    def _create_user(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']

        user = User.objects.create_user(username, email, password)

        account = Account(user=user)
        if hasattr(settings, 'CLOSED_BETA') and not settings.CLOSED_BETA:
            account.beta_access = True
        account.save()

        user.is_active = True
        user.save()

        return user

    def _send_email(self, user):
        domain = get_current_site(self.request).domain
        send_activation_email(user, domain)

    def _login(self, user):
        login(self.request, user)

    def form_valid(self, form):
        user = self._create_user(form)

        self._send_email(user)
        self._login(user)

        return super(RegisterView, self).form_valid(form)

"""
Class based views.

This module will include views for the accounts app.
"""

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView, UpdateView
from django.views import View
from django.contrib.auth import views as auth_views
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.template.response import TemplateResponse
from accounts.models import Profile
from accounts.forms import UserRegistrationForm, ProfileEditForm
from accounts.authentication import send_activation_email, account_activation_token
from django.http import HttpResponseRedirect


class RegisterView(FormView):
    """
    A form view that handles user registration.
    """
    template_name = "accounts/register/register.html"
    form_class = UserRegistrationForm
    success_url = "/"

    def _create_user(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        email = form.cleaned_data["email"]

        user = get_user_model().objects.create_user(username, email, password)
        Profile.objects.create(user=user)

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


class PasswordResetView(auth_views.PasswordResetView):
    template_name = "accounts/users/password_reset.html"
    email_template_name = "accounts/users/password_reset_email.html"
    subject_template_name = "accounts/users/password_reset_subject.txt"
    from_email = settings.EMAIL_HOST_USER
    success_url = reverse_lazy("accounts_password_reset_done")


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "accounts/users/password_reset_done.html"


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "accounts/users/password_reset_confirm.html"
    success_url = reverse_lazy("accounts_password_reset_complete")


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "accounts/users/password_reset_complete.html"


class SettingsView(LoginRequiredMixin, UpdateView):
    """A form view to edit Profile"""

    login_url = 'accounts_login'
    form_class = ProfileEditForm
    success_url = reverse_lazy('accounts_settings')
    template_name = 'accounts/utils/update_settings.html'

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

    def get_initial(self):
        profile = Profile.objects.get(user=self.request.user)
        self.initial.update({
            "username": profile.user.username,
            "email": profile.user.email,
            "first_name": profile.first_name or None,
            "last_name": profile.last_name or None,
            "about_me": profile.about_me or None,
        })
        return super(SettingsView, self).get_initial()


class ProfileActivationView(View):
    """
        This shows different views to the user when they are verifying
        their account based on whether they are already verified or not.
    """
    def get(self, request, uidb64, token):

        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            profile = Profile.objects.get(user=user)
            if profile.is_verified:
                redirect_link = {"href": "/", "label": "Back to Main"}
                template_var = {
                    "title": "Email Already Verified",
                    "content": "You have already verified your email",
                    "link": redirect_link,
                }
                return TemplateResponse(request, "general-message.html", template_var)
            else:
                profile.is_verified = True
                profile.save()

                redirect_link = {"href": "/", "label": "Back to Main"}
                template_var = {
                    "title": "Email Verification Successful",
                    "content": "Thank you for verifying your email with CiviWiki",
                    "link": redirect_link,
                }
                return TemplateResponse(request, "general-message.html", template_var)
        else:
            # invalid link
            redirect_link = {"href": "/", "label": "Back to Main"}
            template_var = {
                "title": "Email Verification Error",
                "content": "Email could not be verified",
                "link": redirect_link,
            }
            return TemplateResponse(request, "general-message.html", template_var)


class ProfileSetupView(LoginRequiredMixin, View):
    """A view to make the user profile full_profile"""

    login_url = 'accounts_login'

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        if profile.full_profile:
            return HttpResponseRedirect("/")
            # start temp rep rendering TODO: REMOVE THIS
        else:
            data = {
                "username": request.user.username,
                "email": request.user.email,
            }
            return TemplateResponse(request, "accounts/user-setup.html", data)

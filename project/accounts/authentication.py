from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.response import TemplateResponse  # TODO: move this out to views
from django.utils.crypto import salted_hmac
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import int_to_base36
from django.template.loader import render_to_string


from accounts.utils import send_email
from .forms import RecoverUserForm


class ProfileActivationTokenGenerator(PasswordResetTokenGenerator):
    """Token Generator for Email Confirmation"""

    key_salt = "django.contrib.auth.tokens.PasswordResetTokenGenerator"

    def _make_token_with_timestamp(self, user, timestamp, legacy=False):
        """ Token function pulled from Django 1.11 """
        ts_b36 = int_to_base36(timestamp)

        hash = salted_hmac(
            self.key_salt, str(user.pk) + str(timestamp)
        ).hexdigest()[::2]
        return "%s-%s" % (ts_b36, hash)


account_activation_token = ProfileActivationTokenGenerator()


def send_activation_email(user, domain):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    base_url = "http://{domain}/activate_account/{uid}/{token}/"
    url_with_code = base_url.format(domain=domain, uid=uid, token=token)
    # Send Email Verification Message
    # TODO: Move this to string templates
    context = {
        "title": "Verify your email with CiviWiki",
        "body": (
            "Welcome to CiviWiki! Follow the link below to verify your email with us. "
            "We're happy to have you on board :)"
        ),
        "link": url_with_code,
    }

    message = render_to_string("email/base_text_template.txt", context)
    html_message = render_to_string("email/base_email_template.html", context)
    sender = settings.EMAIL_HOST_USER
    send_email(
        subject="CiviWiki Profile Setup",
        message=message,
        sender=sender,
        recipient_list=[user.email],
        html_message=html_message
    )


def recover_user():
    """
    USAGE:
        Used to recover a lost username.
    """

    view_variables = {
        "template_name": "user/reset_by_email.html",
        "post_reset_redirect": "recovery_email_sent",
        "email_template_name": "email/base_text_template.txt",
        "subject_template_name": "email/base_email_template.html",
        "password_reset_form": RecoverUserForm,
    }

    return view_variables


def recover_user_sent(request):
    """
    USAGE:
        Displays to the user that the user recover request was sent.
    """

    redirect_link = {"href": "/", "label": "Back to Main"}

    template_var = {
        "title": "Email Sent",
        "content": (
            "We've emailed you your username and instructions for setting your password. "
            "If an account exists with the email you entered, you should receive them shortly. "
            "If you don't receive an email, please make sure you've entered the address you registered with, "
            "and check your spam folder."
        ),
        # TODO: move to string templates
        "link": redirect_link,
    }
    return TemplateResponse(request, "general-message.html", template_var)


def password_reset_complete(request):
    """
    USAGE:
        Displays to the user that their password was reset.
    """

    redirect_link = {"href": "/login", "label": "Login"}

    template_var = {
        "title": "Password reset complete",
        "content": "Your password has been set. You may now go ahead and login.",
        "link": redirect_link,
    }
    return TemplateResponse(request, "general-message.html", template_var)

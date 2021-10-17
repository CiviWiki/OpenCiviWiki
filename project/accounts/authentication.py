from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.crypto import salted_hmac
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import int_to_base36
from django.template.loader import render_to_string
from accounts.utils import send_email


class ProfileActivationTokenGenerator(PasswordResetTokenGenerator):
    """Token Generator for Email Confirmation"""

    key_salt = "django.contrib.auth.tokens.PasswordResetTokenGenerator"

    def _make_token_with_timestamp(self, user, timestamp, legacy=False):
        """Token function pulled from Django 1.11"""
        ts_b36 = int_to_base36(timestamp)

        hash_string = salted_hmac(
            self.key_salt, str(user.pk) + str(timestamp)
        ).hexdigest()[::2]
        return "%s-%s" % (ts_b36, hash_string)


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
        html_message=html_message,
    )

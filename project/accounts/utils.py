from django.conf import settings
from django.core.mail import send_mail



def send_email(subject, message, sender, recipient_list, html_message=None):
    """ A wrapper around Django's send email."""

    # If DEBUG is True or no email host is configured, skip sending the email.
    if (hasattr(settings, 'DEBUG') and settings.DEBUG) or not hasattr(settings, 'EMAIL_HOST'):
        return 0

    return send_mail(
        subject,  # Subject Line
        message,  # text/plain Content
        sender,  # Sender Email (default: support@civiwiki.org)
        recipient_list,  # Target Email
        html_message=html_message,  # text/html Content
    )

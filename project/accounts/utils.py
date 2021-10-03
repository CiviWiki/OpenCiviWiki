from django.core.mail import get_connection, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from accounts.models import Profile


def send_email(subject, message, sender, recipient_list, html_message=None):
    """A wrapper around Django's send email."""

    # If DEBUG is True or no email host is configured, skip sending the email.
    if (hasattr(settings, "DEBUG") and settings.DEBUG) or not hasattr(
        settings, "EMAIL_HOST"
    ):
        return 0

    return send_mail(
        subject,  # Subject Line
        message,  # text/plain Content
        sender,  # Sender Email (default: support@civiwiki.org)
        recipient_list,  # Target Email
        html_message=html_message,  # text/html Content
    )


def send_mass_email(subject, contexts):
    """Construct and send a multipart/alternative email"""

    # Manually open connection to the SMTP server specified in settings.py
    connection = get_connection()  # uses SMTP server specified in settings.py
    connection.open()

    messages = []
    for email_context in contexts:
        msg_plain = render_to_string("email/base_text_template.txt", email_context)
        msg_html = render_to_string("email/base_email_template.html", email_context)

        msg = EmailMultiAlternatives(
            subject,  # Subject Line
            msg_plain,  # text/plain Content
            settings.EMAIL_HOST_USER,  # Sender Email (default: support@civiwiki.org)
            email_context["recipient"],  # Target Email
            connection=connection,
        )
        msg.attach_alternative(msg_html, "text/html")  # text/html Content
        messages.append(msg)

    connection.send_messages(messages)


def get_account(user=None, pk=None, username=None):
    """gets author based on the user"""
    if user:
        return get_object_or_404(Profile, user=user)
    elif pk:
        return get_object_or_404(Profile, pk=pk)
    elif username:
        return get_object_or_404(Profile, user__username=username)

    else:
        raise Http404

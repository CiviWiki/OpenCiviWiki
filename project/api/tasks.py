"""
Tasks to be executed asynchrounsly with Celery

Preface the functions with the @shared_task decorator.
Defined task functions output the returned value to the celery worker console


TODO: move to auth
"""
from __future__ import absolute_import

from django.conf import settings
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import get_connection, EmailMultiAlternatives

@shared_task(name="send_email")
def send_email(subject="", recipient_list="", context=None):
    """ Construct and send a multipart/alternative email """

    if not subject or not recipient_list or not context:
        return "Insufficient values"

    email_context = context

    msg_plain = render_to_string('email/base_text_template.txt', email_context)
    msg_html = render_to_string('email/base_email_template.html', email_context)

    send_mail(
        subject, #Subject Line
        msg_plain, # text/plain Content
        settings.EMAIL_HOST_USER, # Sender Email (default: support@civiwiki.org)
        recipient_list, # Target Email
        html_message=msg_html, # text/html Content
    )

    return "success"


@shared_task(name="send_mass_email")
def send_mass_email(subject="", contexts=None):
    """ Construct and send a multipart/alternative email """

    if not subject or not contexts:
        return "Insufficient values"

    # Manually open connection to the SMTP server specified in settings.py
    connection = get_connection() # uses SMTP server specified in settings.py
    connection.open()

    messages = []
    for email_context in contexts:
        msg_plain = render_to_string('email/base_text_template.txt', email_context)
        msg_html = render_to_string('email/base_email_template.html', email_context)

        msg = EmailMultiAlternatives(
            subject, #Subject Line
            msg_plain, # text/plain Content
            settings.EMAIL_HOST_USER, # Sender Email (default: support@civiwiki.org)
            email_context['recipient'], # Target Email
            connection=connection,
        )
        msg.attach_alternative(msg_html, "text/html")# text/html Content
        messages.append(msg)

    connection.send_messages(messages)

    return "success"

"""
Tasks to be executed asynchrounsly with Celery

Preface the functions with the @shared_task decorator.
Defined task functions output the returned value to the celery worker console


TODO: move to auth
"""
from __future__ import absolute_import

from django.conf import settings
from django.core import mail
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string


@shared_task(name="send_email")
def send_email(subject="", recipient_email="", context=None):
    """ Construct and send a multipart/alternative email """

    if not subject or not recipient_email or not context:
        return "Insufficient values"

    email_context = context

    msg_plain = render_to_string('email/base_text_template.txt', email_context)
    msg_html = render_to_string('email/base_email_template.html', email_context)

    send_mail(
        subject, #Subject Line
        msg_plain, # text/plain Content
        settings.EMAIL_HOST_USER, # Sender Email (default: support@civiwiki.org)
        [recipient_email], # Target Email
        html_message=msg_html, # text/html Content
    )

    return "success"

#def send_text_email()
#def send_html_email()

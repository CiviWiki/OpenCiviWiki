"""
Tasks to be executed asynchrounsly with Celery

Preface the functions with the @shared_task decorator.
Defined task functions output the returned value to the celery worker console
"""
from __future__ import absolute_import

from django.conf import settings
from django.core import mail
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string


@shared_task(name="send_email")
def send_email():
    """ Construct and send a multipart/alternative email """

    some_params = {}
    msg_plain = render_to_string('email/email.txt', {'some_params': some_params})
    msg_html = render_to_string('email/email.html', {'some_params': some_params})

    send_mail(
        'email title', #Subject Line
        msg_plain, # text/plain Content
        settings.EMAIL_HOST_USER, # Sender Email (default: support@civiwiki.org)
        ['some@receiver.com'], # Target Email
        html_message=msg_html, # text/html Content
    )

@shared_task(name="send_email_test")
def send_email_test():
    """ Construct and send a multipart/alternative email """
    email_data = {
        'title': "Example Test Title"
    }
    msg_plain = "This is a test"
    msg_html = render_to_string('email/base_email_template.html', email_data)

    send_mail(
        'email title', #Subject Line
        msg_plain, # text/plain Content
        settings.EMAIL_HOST_USER, # Sender Email (default: support@civiwiki.org)
        ['joohee@civiwiki.org'], # Target Email
        html_message=msg_html, # text/html Content
    )

"""
WSGI config for civiwiki project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""
from __future__ import unicode_literals
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "civiwiki.settings")
application = get_wsgi_application()
application = DjangoWhiteNoise(application)

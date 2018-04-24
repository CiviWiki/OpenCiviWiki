from __future__ import unicode_literals
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=63)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

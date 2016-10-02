from django.db import models
from category import Category


class Topic(models.Model):
    category = models.ForeignKey(Category, default=None, null=True)
    name = models.CharField(max_length=63)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

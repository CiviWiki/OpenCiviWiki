from django.db import models

class Hashtag(models.Model):
    name = models.CharField(max_length=63)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

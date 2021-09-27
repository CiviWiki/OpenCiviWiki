from django.db import models

# Create your models here.
"""

Category Model

"""


class Category(models.Model):
    name = models.CharField(max_length=63)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

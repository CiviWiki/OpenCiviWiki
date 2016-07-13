from __future__ import unicode_literals
from django.db import models
import datetime, json

from django.contrib.auth.models import Group, Permission

class GroupManager(models.Manager):
    def summarize(self, group):
        return {
            "title": group.title,
            "profile_image": group.profile_image
        }

    def serialize(self, group):
        from account import Account
        data = {
            "title": group.title,
            "description": group.description,
            "profile_image": group.profile_image,
            "cover_image": group.cover_image
        }
        return json.dumps(data)

class GroupMeta(models.Model):
    objects = GroupManager()
    group = models.ForeignKey(Group, related_name='group')
    title = models.CharField(max_length=63)
    description = models.TextField(max_length=4095)
    profile_image = models.CharField(max_length=255)
    cover_image = models.CharField(max_length=255)

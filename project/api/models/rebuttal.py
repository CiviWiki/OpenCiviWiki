"""
Rebuttal model
Extends local Profile and Response model
"""

from django.db import models

from accounts.models import Profile
from .response import Response


class Rebuttal(models.Model):
    author = models.ForeignKey(
        Profile, default=None, null=True, on_delete=models.PROTECT
    )
    response = models.ForeignKey(
        Response, default=None, null=True, on_delete=models.PROTECT
    )

    body = models.TextField(max_length=1023)

    votes_vneg = models.IntegerField(default=0)
    votes_neg = models.IntegerField(default=0)
    votes_neutral = models.IntegerField(default=0)
    votes_pos = models.IntegerField(default=0)
    votes_vpos = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

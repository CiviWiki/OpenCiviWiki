from django.db import models
from account import Account
from response import Response

class Rebuttal(models.Model):
    author = models.ForeignKey(Account, default=None, null=True)
    response = models.ForeignKey(Response, default=None, null=True)

    body = models.TextField(max_length=1023)

    votes_vneg = models.IntegerField(default=0)
    votes_neg = models.IntegerField(default=0)
    votes_neutral = models.IntegerField(default=0)
    votes_pos = models.IntegerField(default=0)
    votes_vpos = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

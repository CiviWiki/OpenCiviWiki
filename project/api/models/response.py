from django.db import models
from account import Account
from civi import Civi

class Response(models.Model):
    author = models.ForeignKey(Account, default=None, null=True)
    civi = models.ForeignKey(Civi, default=None, null=True)

    title = models.CharField(max_length=127)
    body = models.TextField(max_length=2047)

    votes_vneg = models.IntegerField(default=0)
    votes_neg = models.IntegerField(default=0)
    votes_neutral = models.IntegerField(default=0)
    votes_pos = models.IntegerField(default=0)
    votes_vpos = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

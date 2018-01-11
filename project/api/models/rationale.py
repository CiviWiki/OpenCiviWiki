from django.db import models

from .bill import Bill
from .representative import Representative
from .vote import Vote


class Rationale(models.Model):
    bill = models.ForeignKey(Bill, default=None, null=True)
    representative = models.ForeignKey(Representative, default=None, null=True)
    vote = models.ForeignKey(Vote, default=None, null=True)

    title = models.CharField(max_length=127)
    body = models.TextField(max_length=4095)

    votes_vneg = models.IntegerField(default=0)
    votes_neg = models.IntegerField(default=0)
    votes_neutral = models.IntegerField(default=0)
    votes_pos = models.IntegerField(default=0)
    votes_vpos = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

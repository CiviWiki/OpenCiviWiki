from django.db import models
from account import Account
from thread import Thread
from bill import Bill
from hashtag import Hashtag
# from django.contrib.postgres.fields import ArrayField


class Civi(models.Model):
    author = models.ForeignKey(Account, default=None, null=True)
    thread = models.ForeignKey(Thread, default=None, null=True)
    bill = models.ForeignKey(Bill, default=None, null=True) # null if not solution

    hashtags = models.ManyToManyField(Hashtag)

    parents = models.ManyToManyField('self') # 0 if c_type == problem

    title = models.CharField(max_length=127)
    body = models.CharField(max_length=4095)

    c_CHOICES = (
        ('problem', 'Problem'),
        ('cause', 'Cause'),
        ('solution', 'Solution'),
    )
    c_type = models.CharField(max_length=31, default='problem', choices=c_CHOICES)

    # sources = ArrayField(models.CharField(max_length=127, blank=True), default=[], blank=True)
    # attachments

    votes_vneg = models.IntegerField(default=0)
    votes_neg = models.IntegerField(default=0)
    votes_neutral = models.IntegerField(default=0)
    votes_pos = models.IntegerField(default=0)
    votes_vpos = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

from django.db import models
from account import Account
from civi import Civi
from thread import Thread

class ActivityManager(models.Manager):
    def votes(self, civi_id):
        civi = Civi.objects.get(id=civi_id)
        votes = dict(
            votes_vneg=civi.votes_vneg,
            votes_neg=civi.votes_neg,
            votes_neutral=civi.votes_neutral,
            votes_pos=civi.votes_pos,
            votes_vpos=civi.votes_vpos
        )
        return votes


class Activity(models.Model):
    account = models.ForeignKey(Account, default=None, null=True)
    thread = models.ForeignKey(Thread, default=None, null=True)
    civi = models.ForeignKey(Civi, default=None, null=True)

    activity_CHOICES = (
        ('vote_vneg', 'Vote Strongly Disagree'),
        ('vote_neg', 'Vote Disagree'),
        ('vote_neutral', 'Vote Neutral'),
        ('vote_pos', 'Vote Agree'),
        ('vote_vpos', 'Vote Strongly Agree'),
        ('favorite', 'Favor a Civi')
    )
    activity_type = models.CharField(max_length=255, choices=activity_CHOICES)

    read = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

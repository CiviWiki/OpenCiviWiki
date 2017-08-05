from django.db import models
from account import Account
from civi import Civi
from thread import Thread


class Notification(models.Model):
    account = models.ForeignKey(Account, default=None, null=True)
    thread = models.ForeignKey(Thread, default=None, null=True)
    civi = models.ForeignKey(Civi, default=None, null=True) # always a solution or null

    # Need to go to bed but there are going to be SO MANY OF THESE
    activity_CHOICES = (
        ('new_follower', 'New follower'),
        ('response_to_yout_civi', 'Response to your civi'),
        ('rebuttal_to_your_response', 'Rebuttal to your response'),
    )
    activity_type = models.CharField(max_length=31, default='new_follower', choices=activity_CHOICES)
    read = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

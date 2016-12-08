from django.db import models
from account import Account
from thread import Thread
from bill import Bill
from hashtag import Hashtag
import random as r
import json
from django.core.serializers.json import DjangoJSONEncoder
from calendar import month_name

class CiviManager(models.Manager):
    def summarize(self, civi):
        return {
            "id": civi.id,
            "type": civi.c_type,
            "title": civi.title,
            "body": civi.body[0:150]
        }

    def serialize(self, civi, filter=None):
        data = {
            "type": civi.c_type,
            "title": civi.title,
            "body": civi.body,
            "attachments": [],
            "author": dict(username=civi.author.user.username, profile_image=civi.author.profile_image.url),
            "hashtags": [h.title for h in civi.hashtags.all()],
            "created": "{0} {1}, {2}".format(month_name[civi.created.month], civi.created.day, civi.created.year),
            "ratings": [r.randint(0,50) for x in range(5)], #TODO: real points
            "id": civi.id
	    }

        if filter and filter in data:
            return json.dumps({filter: data[filter]})
        return json.dumps(data, cls=DjangoJSONEncoder)


class Civi(models.Model):
    objects = CiviManager()
    author = models.ForeignKey(Account, default=None, null=True)
    thread = models.ForeignKey(Thread, default=None, null=True)
    bill = models.ForeignKey(Bill, default=None, null=True) # null if not solution

    hashtags = models.ManyToManyField(Hashtag)

    links = models.ManyToManyField('self')

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

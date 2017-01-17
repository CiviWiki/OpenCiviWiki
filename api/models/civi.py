from django.db import models
from account import Account
from thread import Thread
from bill import Bill
from hashtag import Hashtag
import random as r
import json, datetime, math
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
            "author": dict(
                username=civi.author.user.username,
                profile_image=civi.author.profile_image.url,
                first_name=civi.author.first_name,
                last_name=civi.author.last_name
            ),
            "hashtags": [h.title for h in civi.hashtags.all()],
            "created": "{0} {1}, {2}".format(month_name[civi.created.month], civi.created.day, civi.created.year),
            "attachments": [],
            "votes": civi.votes(),
            "id": civi.id,
            "thread_id": civi.thread.id
	    }

        if filter and filter in data:
            return json.dumps({filter: data[filter]})
        return json.dumps(data, cls=DjangoJSONEncoder)

    def serialize_s(self, civi, filter=None):
        data = {
            "type": civi.c_type,
            "title": civi.title,
            "body": civi.body,
            "author": dict(
                username=civi.author.user.username,
                profile_image= civi.author.profile_image.url if civi.author.profile_image else "/media/profile/default.png",
                first_name=civi.author.first_name,
                last_name=civi.author.last_name
            ),
            "hashtags": [h.title for h in civi.hashtags.all()],
            "created": "{0} {1}, {2}".format(month_name[civi.created.month], civi.created.day, civi.created.year),
            "attachments": [],
            "votes": civi.votes(),
            "id": civi.id,
            "thread_id": civi.thread.id,
            "links": [c for c in civi.linked_civis.all().values_list('id', flat=True)]
	    }

        if filter and filter in data:
            return json.dumps({filter: data[filter]})
        return data



class Civi(models.Model):
    objects = CiviManager()
    author = models.ForeignKey(Account, default=None, null=True)
    thread = models.ForeignKey(Thread, default=None, null=True)
    bill = models.ForeignKey(Bill, default=None, null=True) # null if not solution

    hashtags = models.ManyToManyField(Hashtag)

    linked_civis = models.ManyToManyField('self', related_name="links")
    response_civis = models.ForeignKey('self', related_name="responses", default=None, null=True) #TODO: Probably remove this

    title = models.CharField(max_length=255, blank=False, null=False)
    body = models.CharField(max_length=1023, blank=False, null=False)

    c_CHOICES = (
        ('problem', 'Problem'),
        ('cause', 'Cause'),
        ('solution', 'Solution'),
        ('response', 'Response'), #TODO: move this to separate model O
    )
    c_type = models.CharField(max_length=31, default='problem', choices=c_CHOICES)

    # sources = ArrayField(models.CharField(max_length=127, blank=True), default=[], blank=True)
    # attachments

    votes_vneg = models.IntegerField(default=0)
    votes_neg = models.IntegerField(default=0)
    votes_neutral = models.IntegerField(default=0)
    votes_pos = models.IntegerField(default=0)
    votes_vpos = models.IntegerField(default=0)

    def votes(self):
        from activity import Activity
        act_votes = Activity.objects.filter(civi=self)
        # votes = dict(
        #     votes_vneg = self.votes_vneg,
        #     votes_neg = self.votes_neg,
        #     votes_neutral = self.votes_neutral,
        #     votes_pos = self.votes_pos,
        #     votes_vpos = self.votes_vpos
        # )
        votes = dict(
            total = act_votes.count() - act_votes.filter(activity_type='vote_neutral').count(),
            votes_vneg = act_votes.filter(activity_type='vote_vneg').count(),
            votes_neg = act_votes.filter(activity_type='vote_neg').count(),
            votes_neutral = act_votes.filter(activity_type='vote_neutral').count(),
            votes_pos = act_votes.filter(activity_type='vote_pos').count(),
            votes_vpos = act_votes.filter(activity_type='vote_vpos').count()
        )
        return votes

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    def score(self, request_acct_id):
        SD = -2
        D = -1
        A = 1
        SA = 2
        owner_id = self.author
        post_time = self.created
        current_time = datetime.datetime.now()


        account = Account.objects.get(id=request_acct_id)

        #step 1
        votes = self.votes()
        v = votes['total']
        x = votes['votes_vneg'] * SD + votes['votes_neg'] * D + votes['votes_pos'] * A + votes['votes_vpos'] * SA
        y = (1 if self.author in account.following.all().values_list('id', flat=True) else 0)
        f = 0 #TODO: favorite val
        t = (current_time - post_time.replace(tzinfo=None)).total_seconds()
        g = 2

        #step2
        if x > 0:
            #step3 - A X*Log10V+Y + F + (##/T) = Rank Value
            rank = x * math.log10(v) + y + f + g/t

        elif x == 0:
            #step3 - B  V^2+Y + F + (##/T) = Rank Value
            rank = v**2 + y + f + g/t
        elif x < 0:
            #step3 - C
            if abs(x)/v <= 5:
                rank = abs(x) * math.log10(v) + y + f + g/t
            else:
                rank = x * math.log10(v) + y + f + g/t

        return rank

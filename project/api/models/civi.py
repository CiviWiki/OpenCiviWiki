from django.db import models
from .account import Account
from .thread import Thread
from .bill import Bill
from .hashtag import Hashtag
import random as r
import os, json, datetime, math, uuid
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.deconstruct import deconstructible
from django.core.files.storage import default_storage
from django.conf import settings
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
            "author": {
                'username': civi.author.user.username,
                'profile_image': civi.author.profile_image_url,
                'first_name': civi.author.first_name,
                'last_name': civi.author.last_name
            },
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
                profile_image=civi.author.profile_image.url if civi.author.profile_image else "/media/profile/default.png",
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

    def thread_sorted_by_score(self, civis_qs, req_acct_id):
        qs = civis_qs.order_by('-created')
        return sorted(qs.all(), key=lambda c: c.score(req_acct_id), reverse=True)


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
        ('response', 'Response'), #TODO: move this to separate model (subclass?)
        ('rebuttal', 'Rebuttal'),
    )
    c_type = models.CharField(max_length=31, default='problem', choices=c_CHOICES)

    votes_vneg = models.IntegerField(default=0)
    votes_neg = models.IntegerField(default=0)
    votes_neutral = models.IntegerField(default=0)
    votes_pos = models.IntegerField(default=0)
    votes_vpos = models.IntegerField(default=0)

    def votes(self):
        from activity import Activity
        act_votes = Activity.objects.filter(civi=self)

        votes = {
            'total': act_votes.count() - act_votes.filter(activity_type='vote_neutral').count(),
            'votes_vneg': act_votes.filter(activity_type='vote_vneg').count(),
            'votes_neg': act_votes.filter(activity_type='vote_neg').count(),
            'votes_neutral': act_votes.filter(activity_type='vote_neutral').count(),
            'votes_pos': act_votes.filter(activity_type='vote_pos').count(),
            'votes_vpos': act_votes.filter(activity_type='vote_vpos').count()
        }
        return votes

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    # Allow draft state Civis (default to True)
    is_draft = models.BooleanField(default=True)

    def _get_created_date_str(self):
        d = self.created
        return "{0} {1}, {2}".format(month_name[d.month], d.day, d.year)
    created_date_str = property(_get_created_date_str)

    def score(self, request_acct_id=None):
        SD = -2
        D = -1
        A = 1
        SA = 2

        post_time = self.created
        current_time = datetime.datetime.now()

        #step 1
        votes = self.votes()
        v = votes['total']
        x = votes['votes_vneg'] * SD + votes['votes_neg'] * D + votes['votes_pos'] * A + votes['votes_vpos'] * SA
        if request_acct_id:
            account = Account.objects.get(id=request_acct_id)
            y = (1 if self.author in account.following.all().values_list('id', flat=True) else 0)
        else:
            y = 0

        f = 0 #TODO: favorite val
        t = (current_time - post_time.replace(tzinfo=None)).total_seconds() / 300
        g = 1
        amp = math.pow(10,0)
        #step2
        if x > 0:
            v = votes['total'] if votes['total'] > 1 else 2
            #step3 - A X*Log10V+Y + F + (##/T) = Rank Value
            rank = x * math.log10(v) * amp + y + f + g/t

        elif x == 0:

            #step3 - B  V^2+Y + F + (##/T) = Rank Value
            rank = v**2 + y + f + g/t
        elif x < 0:
            v = votes['total'] if votes['total'] > 1 else 2
            #step3 - C
            if abs(x)/v <= 5:
                rank = abs(x) * math.log10(v) * amp + y + f + g/t
            else:
                rank = x * math.log10(v) * amp + y + f + g/t
        return rank

    def dict_with_score(self, req_acct_id=None):
        data = {
            "id": self.id,
            "thread_id": self.thread.id,
            "type": self.c_type,
            "title": self.title,
            "body": self.body,
            "author": {
                'username': self.author.user.username,
                'profile_image': self.author.profile_image_url,
                'first_name': self.author.first_name,
                'last_name': self.author.last_name
            },
            "votes": self.votes(),
            "links": [c for c in self.linked_civis.all().values_list('id', flat=True)],
            "created": self.created_date_str,
            # Not Implemented Yet
            "hashtags": [],
            "attachments": [{'id': img.id, 'url': img.image_url} for img in self.images.all()],
        }
        if req_acct_id:
            data['score'] = self.score(req_acct_id)

        return data


@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        new_filename = str(uuid.uuid4())
        filename = '{}.{}'.format(new_filename, ext)
        return os.path.join(self.sub_path, filename)


image_upload_path = PathAndRename('')

class CiviImageManager(models.Manager):
    def get_images(self):
        return

class CiviImage(models.Model):
    objects = CiviImageManager()
    civi = models.ForeignKey(Civi, related_name='images')
    title = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to=image_upload_path, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def _get_image_url(self):
        if self.image and default_storage.exists(os.path.join(settings.MEDIA_ROOT, self.image.name)):
            return self.image.url
        else:
            #NOTE: This default url will probably be changed later
            return "/static/img/no_image_md.png",
    image_url = property(_get_image_url)

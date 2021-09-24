import os
import json
import math
import datetime
from calendar import month_name

from accounts.models import Profile
from common.utils import PathAndRename
from core.constants import CIVI_TYPES, US_STATES
from django.conf import settings
from django.core.files.storage import default_storage
from django.db import models
from taggit.managers import TaggableManager
from django.core.serializers.json import DjangoJSONEncoder


class Fact(models.Model):
    body = models.CharField(max_length=511)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

class ThreadManager(models.Manager):
    # TODO: move this to read.py, try to be more query operation specific here
    def summarize(self, thread):
        # Number of characters after which to truncate thread
        thread_truncate_length = 320

        # If thread length is longer than truncate length... add elipsis (truncate)
        ellipsis_if_too_long = (
            "" if len(thread.summary) <= thread_truncate_length else "..."
        )

        thread_data = {
            "id": thread.id,
            "title": thread.title,
            "summary": thread.summary[:thread_truncate_length] + (ellipsis_if_too_long),
            "created": "{0} {1}, {2}".format(
                month_name[thread.created.month],
                thread.created.day,
                thread.created.year,
            ),
            "category_id": thread.category.id,
            "location": thread.level
            if not thread.state
            else dict(US_STATES).get(thread.state),
            "image": thread.image_url,
        }
        author_data = {
            "username": thread.author.user.username,
            "full_name": thread.author.full_name,
            "profile_image": thread.author.profile_image_url,
        }
        stats_data = {
            "num_views": thread.num_views,
            "num_civis": Civi.objects.all()
            .filter(thread_id=thread.id)
            .count(),  # thread.num_civis,
            "num_solutions": thread.num_solutions,
        }

        data = {"thread": thread_data, "author": author_data, "stats": stats_data}
        return data

    def filter_by_category(self, categories):
        return self.all().filter(category__in=categories)


image_upload_path = PathAndRename("")


class Thread(models.Model):
    author = models.ForeignKey(
        Profile, default=None, null=True, on_delete=models.PROTECT
    )
    category = models.ForeignKey(
        Category, default=None, null=True, on_delete=models.PROTECT
    )
    facts = models.ManyToManyField(Fact)

    tags = TaggableManager()

    title = models.CharField(max_length=127, blank=False, null=False)
    summary = models.CharField(max_length=4095, blank=False, null=False)
    image = models.ImageField(upload_to=image_upload_path, blank=True, null=True)

    level_CHOICES = (
        ("federal", "Federal"),
        ("state", "State"),
    )
    level = models.CharField(max_length=31, default="federal", choices=level_CHOICES)
    state = models.CharField(max_length=2, choices=US_STATES, blank=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    @property
    def image_url(self):  # TODO: move this to utils
        if self.image and default_storage.exists(
            os.path.join(settings.MEDIA_ROOT, self.image.name)
        ):
            return self.image.url
        else:
            # NOTE: This default url will probably be changed later
            return "/static/img/no_image_md.png"

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    # Allow draft stage threads (default to True)
    is_draft = models.BooleanField(default=True)

    num_views = models.IntegerField(default=0)
    num_civis = models.IntegerField(default=0)
    num_solutions = models.IntegerField(default=0)

    objects = ThreadManager()

    @property
    def created_date_str(self):
        d = self.created
        return "{0} {1}, {2}".format(month_name[d.month], d.day, d.year)


class CiviManager(models.Manager):
    def summarize(self, civi):
        return {
            "id": civi.id,
            "type": civi.c_type,
            "title": civi.title,
            "body": civi.body[0:150],
        }

    def serialize(self, civi, filter=None):
        data = {
            "type": civi.c_type,
            "title": civi.title,
            "body": civi.body,
            "author": {
                "username": civi.author.user.username,
                "profile_image": civi.author.profile_image_url,
                "first_name": civi.author.first_name,
                "last_name": civi.author.last_name,
            },
            "tags": [tag.title for tag in civi.tags.all()],
            "created": "{0} {1}, {2}".format(
                month_name[civi.created.month], civi.created.day, civi.created.year
            ),
            "attachments": [],
            "votes": civi.votes,
            "id": civi.id,
            "thread_id": civi.thread.id,
        }

        if filter and filter in data:
            return json.dumps({filter: data[filter]})
        return json.dumps(data, cls=DjangoJSONEncoder)

    def serialize_s(self, civi, filter=None):
        # Get profile profile image, or set to default image
        profile_image_or_default = (
            civi.author.profile_image.url or "/media/profile/default.png"
        )

        data = {
            "type": civi.c_type,
            "title": civi.title,
            "body": civi.body,
            "author": dict(
                username=civi.author.user.username,
                profile_image=profile_image_or_default,
                first_name=civi.author.first_name,
                last_name=civi.author.last_name,
            ),
            "tags": [h.title for h in civi.tags.all()],
            "created": "{0} {1}, {2}".format(
                month_name[civi.created.month], civi.created.day, civi.created.year
            ),
            "attachments": [],
            "votes": civi.votes,
            "id": civi.id,
            "thread_id": civi.thread.id,
            "links": [
                civi for civi in civi.linked_civis.all().values_list("id", flat=True)
            ],
        }

        if filter and filter in data:
            return json.dumps({filter: data[filter]})
        return data

    def thread_sorted_by_score(self, civis_queryset, req_acct_id):
        queryset = civis_queryset.order_by("-created")
        return sorted(queryset.all(), key=lambda c: c.score(req_acct_id), reverse=True)


class Civi(models.Model):
    objects = CiviManager()
    author = models.ForeignKey(
        Profile, related_name="civis", default=None, null=True, on_delete=models.PROTECT
    )
    thread = models.ForeignKey(
        Thread, related_name="civis", default=None, null=True, on_delete=models.PROTECT
    )

    tags = TaggableManager()

    linked_civis = models.ManyToManyField("self", related_name="links")
    response_civis = models.ForeignKey(
        "self",
        related_name="responses",
        default=None,
        null=True,
        on_delete=models.PROTECT,
    )  # TODO: Probably remove this

    title = models.CharField(max_length=255, blank=False, null=False)
    body = models.CharField(max_length=1023, blank=False, null=False)

    c_type = models.CharField(max_length=31, default="problem", choices=CIVI_TYPES)

    votes_vneg = models.IntegerField(default=0)
    votes_neg = models.IntegerField(default=0)
    votes_neutral = models.IntegerField(default=0)
    votes_pos = models.IntegerField(default=0)
    votes_vpos = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def _get_votes(self):
        activity_votes = Activity.objects.filter(civi=self)

        votes = {
            "total": activity_votes.count()
            - activity_votes.filter(activity_type="vote_neutral").count(),
            "votes_vneg": activity_votes.filter(activity_type="vote_vneg").count(),
            "votes_neg": activity_votes.filter(activity_type="vote_neg").count(),
            "votes_neutral": activity_votes.filter(
                activity_type="vote_neutral"
            ).count(),
            "votes_pos": activity_votes.filter(activity_type="vote_pos").count(),
            "votes_vpos": activity_votes.filter(activity_type="vote_vpos").count(),
        }
        return votes

    votes = property(_get_votes)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    @property
    def created_date_str(self):
        d = self.created
        return "{0} {1}, {2}".format(month_name[d.month], d.day, d.year)

    def score(self, request_acct_id=None):
        # TODO: add docstring comment describing this score function in relatively plain English
        # include descriptions of all variables

        # Weights for different vote types
        vneg_weight = -2
        neg_weight = -1
        pos_weight = 1
        vpos_weight = 2

        owner_id = self.author
        post_time = self.created
        current_time = datetime.datetime.now()

        # Get all votes
        votes = self.votes

        # Score each each type of vote, based on count for that type
        vneg_score = votes["votes_vneg"] * vneg_weight
        neg_score = votes["votes_neg"] * neg_weight
        pos_score = votes["votes_pos"] * pos_weight
        vpos_score = votes["votes_vpos"] * vpos_weight

        # Sum up all of the scores
        scores_sum = vneg_score + neg_score + pos_score + vpos_score

        if request_acct_id:
            profile = Profile.objects.get(id=request_acct_id)
            scores_sum = (
                1
                if self.author in profile.following.all().values_list("id", flat=True)
                else 0
            )
        else:
            scores_sum = 0

        favorite = 0

        # Calculate how long ago the post was created
        time_ago = (current_time - post_time.replace(tzinfo=None)).total_seconds() / 300

        gravity = 1  # TODO: determine what the variable 'g' does
        amp = math.pow(10, 0)

        # Calculate rank based on positive, zero, or negative scores sum
        if scores_sum > 0:
            # TODO: determine why we set votes total to two when votes['total'] is <= 1
            # set votes total to 2 when votes['total'] is <= 1
            votes_total = votes["total"] if votes["total"] > 1 else 2

            # step3 - A X*Log10V+Y + F + (##/T) = Rank Value
            rank = (
                scores_sum * math.log10(votes_total) * amp
                + scores_sum
                + favorite
                + gravity / time_ago
            )

        elif scores_sum == 0:
            # Get count of total votes
            votes_total = votes["total"]

            # step3 - B  V^2+Y + F + (##/T) = Rank Value
            rank = votes_total ** 2 + scores_sum + favorite + gravity / time_ago
        elif scores_sum < 0:
            # TODO: determine why we set votes total to two when votes['tota'] is <= 1
            # set votes total to 2 when votes['total'] is <= 1
            votes_total = votes["total"] if votes["total"] > 1 else 2

            # step3 - C
            if abs(scores_sum) / votes_total <= 5:
                rank = (
                    abs(scores_sum) * math.log10(votes_total) * amp
                    + scores_sum
                    + favorite
                    + gravity / time_ago
                )
            else:
                rank = (
                    scores_sum * math.log10(votes_total) * amp
                    + scores_sum
                    + favorite
                    + gravity / time_ago
                )

        return rank

    def dict_with_score(self, req_acct_id=None):
        data = {
            "id": self.id,
            "thread_id": self.thread.id,
            "type": self.c_type,
            "title": self.title,
            "body": self.body,
            "author": {
                "username": self.author.user.username,
                "profile_image": self.author.profile_image_url,
                "profile_image_thumb_url": self.author.profile_image_thumb_url,
                "first_name": self.author.first_name,
                "last_name": self.author.last_name,
            },
            "votes": self.votes,
            "links": [
                civi for civi in self.linked_civis.all().values_list("id", flat=True)
            ],
            "created": self.created_date_str,
            # Not Implemented Yet
            "tags": [],
            "attachments": [
                {"id": img.id, "url": img.image_url} for img in self.images.all()
            ],
        }
        if req_acct_id:
            data["score"] = self.score(req_acct_id)

        return data


class Notification(models.Model):
    account = models.ForeignKey(
        Profile, default=None, null=True, on_delete=models.PROTECT
    )
    thread = models.ForeignKey(
        Thread, default=None, null=True, on_delete=models.PROTECT
    )
    civi = models.ForeignKey(
        Civi, default=None, null=True, on_delete=models.PROTECT
    )  # always a solution or null

    # Need to go to bed but there are going to be SO MANY OF THESE
    activity_CHOICES = (
        ("new_follower", "New follower"),
        ("response_to_yout_civi", "Response to your civi"),
        ("rebuttal_to_your_response", "Rebuttal to your response"),
    )
    activity_type = models.CharField(
        max_length=31, default="new_follower", choices=activity_CHOICES
    )
    read = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)


class Rationale(models.Model):
    title = models.CharField(max_length=127)
    body = models.TextField(max_length=4095)

    votes_vneg = models.IntegerField(default=0)
    votes_neg = models.IntegerField(default=0)
    votes_neutral = models.IntegerField(default=0)
    votes_pos = models.IntegerField(default=0)
    votes_vpos = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)


class Response(models.Model):
    author = models.ForeignKey(
        Profile, default=None, null=True, on_delete=models.PROTECT
    )
    civi = models.ForeignKey(Civi, default=None, null=True, on_delete=models.PROTECT)

    title = models.CharField(max_length=127)
    body = models.TextField(max_length=2047)

    votes_vneg = models.IntegerField(default=0)
    votes_neg = models.IntegerField(default=0)
    votes_neutral = models.IntegerField(default=0)
    votes_pos = models.IntegerField(default=0)
    votes_vpos = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)


image_upload_path = PathAndRename("")


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


class CiviImageManager(models.Manager):
    def get_images(self):
        return


class CiviImage(models.Model):
    objects = CiviImageManager()
    civi = models.ForeignKey(Civi, related_name="images", on_delete=models.PROTECT)
    title = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to=image_upload_path, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    @property
    def image_url(self):
        if self.image and default_storage.exists(
            os.path.join(settings.MEDIA_ROOT, self.image.name)
        ):
            return self.image.url
        else:
            # NOTE: This default url will probably be changed later
            return "/static/img/no_image_md.png"


class ActivityManager(models.Manager):
    def votes(self, civi_id):
        civi = Civi.objects.get(id=civi_id)
        votes = dict(
            votes_vneg=civi.votes_vneg,
            votes_neg=civi.votes_neg,
            votes_neutral=civi.votes_neutral,
            votes_pos=civi.votes_pos,
            votes_vpos=civi.votes_vpos,
        )
        return votes


class Activity(models.Model):
    account = models.ForeignKey(
        Profile, default=None, null=True, on_delete=models.PROTECT
    )
    thread = models.ForeignKey(
        Thread, default=None, null=True, on_delete=models.PROTECT
    )
    civi = models.ForeignKey(Civi, default=None, null=True, on_delete=models.PROTECT)

    activity_CHOICES = (
        ("vote_vneg", "Vote Strongly Disagree"),
        ("vote_neg", "Vote Disagree"),
        ("vote_neutral", "Vote Neutral"),
        ("vote_pos", "Vote Agree"),
        ("vote_vpos", "Vote Strongly Agree"),
        ("favorite", "Favor a Civi"),
    )
    activity_type = models.CharField(max_length=255, choices=activity_CHOICES)

    read = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    @property
    def is_positive_vote(self):
        return self.activity_type.endswith("pos")

    @property
    def is_negative_vote(self):
        return self.activity_type.endswith("neg")

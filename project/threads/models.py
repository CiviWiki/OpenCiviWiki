import datetime
import json
import math
import os
from calendar import month_name
from typing import Any, Dict, List, Tuple

from categories.models import Category
from common.utils import PathAndRename
from core.constants import CIVI_TYPES
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from taggit.managers import TaggableManager


class Fact(models.Model):
    body = models.CharField(max_length=511)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)


class ThreadManager(models.Manager):
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
            "created": f"""{month_name[thread.created.month]}
                            {thread.created.day},
                            {thread.created.year}""",
            "category_id": thread.category.id,
            "image": thread.image_url,
        }
        author_data = {
            "username": thread.author.username,
            "full_name": thread.author.profile.full_name,
            "profile_image": thread.author.profile.profile_image_url,
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


class Thread(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        default=None,
        null=True,
        on_delete=models.PROTECT,
        related_name="threads",
    )
    category = models.ForeignKey(
        Category,
        default=None,
        null=True,
        on_delete=models.PROTECT,
        related_name="threads",
    )
    facts = models.ManyToManyField(Fact)

    tags = TaggableManager()

    title = models.CharField(max_length=127, blank=False, null=False)
    summary = models.CharField(max_length=4095, blank=False, null=False)
    image = models.ImageField(
        upload_to=PathAndRename("thread_uploads"), blank=True, null=True
    )

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
    num_civis = models.IntegerField(default=0)  # TODO To be dropped
    num_solutions = models.IntegerField(default=0)  # TODO To be dropped

    objects = ThreadManager()

    @property
    def created_date_str(self):
        d = self.created
        return f"{month_name[d.month]} {d.day}, {d.year}"

    @property
    def contributors(self):
        return get_user_model().objects.filter(
            pk__in=self.civis.order_by("-created")
            .values_list("author", flat=True)
            .order_by("author")
            .distinct()
        )

    @property
    def problem_civis(self):
        return self.civis.filter(c_type="problem")

    @property
    def cause_civis(self):
        return self.civis.filter(c_type="cause")

    @property
    def solution_civis(self):
        return self.civis.filter(c_type="solution")


class CiviManager(models.Manager):
    def summarize(self, civi):
        return {
            "id": civi.id,
            "type": civi.c_type,
            "title": civi.title,
            "body": civi.body[:150],
        }

    def serialize(self, civi, filter=None):
        data = {
            "type": civi.c_type,
            "title": civi.title,
            "body": civi.body,
            "author": {
                "username": civi.author.username,
                "profile_image": civi.author.profile.profile_image_url,
                "first_name": civi.author.first_name,
                "last_name": civi.author.last_name,
            },
            "tags": [tag.title for tag in civi.tags.all()],
            "created": f"""{month_name[civi.created.month]}
                            {civi.created.day},
                            {civi.created.year}""",
            "attachments": [],
            "votes": civi.votes,
            "id": civi.id,
            "thread_id": civi.thread.id,
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
                username=civi.author.username,
                profile_image=civi.author.profile.profile_image_url,
                first_name=civi.author.first_name,
                last_name=civi.author.last_name,
            ),
            "tags": [h.title for h in civi.tags.all()],
            "created": f"""{month_name[civi.created.month]}
                            {civi.created.day},
                            {civi.created.year}""",
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

    def thread_sorted_by_score(self, civis_queryset, requested_user_id):
        queryset = civis_queryset.order_by("-created")
        return sorted(
            queryset.all(), key=lambda c: c.score(requested_user_id), reverse=True
        )


class Civi(models.Model):
    objects = CiviManager()
    author = models.ForeignKey(
        get_user_model(),
        related_name="civis",
        default=None,
        null=True,
        on_delete=models.PROTECT,
    )
    thread = models.ForeignKey(
        Thread,
        related_name="civis",
        default=None,
        null=True,
        on_delete=models.PROTECT,
    )

    tags = TaggableManager()

    linked_civis = models.ManyToManyField("self", related_name="links", symmetrical=False, blank=True)

    title = models.CharField(max_length=255, blank=False, null=False)
    body = models.CharField(max_length=1023, blank=False, null=False)

    # todo rename to civi_type??
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

    def __node__(self, with_score=False) -> Tuple[List[int], Dict[str, Any]]:
        """
        Documentation:
        Add to a graph like this:
        ```python
        import networkx as nx
        G = nx.DiGraph()
        a_civi = Civi.objects.first()
        node_args, node_kwargs = a_civi.__node__()
        G.add_node(*node_args, **node_kwargs)
        ```
        Args:
            with_score (bool, optional): Defaults to False.

        Returns:
            Tuple[List[int], Dict[str, Any]]: The args and kwargs to be sent to the nx graph `add_node` function
        """
        node_kwargs = {
            'label':self.title,
            'type':self.c_type
        }
        if with_score:
            node_kwargs.update({"score":self.score(), "weight":self.__weight__()})
        return [self.id], node_kwargs

    def __weight__(self):
        return 1 / (1 + self.score())

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
        return f"{month_name[d.month]} {d.day}, {d.year}"

    def score(self, requested_user_id=None):
        # TODO: add docstring comment describing this score function
        # in relatively plain English
        # include descriptions of all variables

        # Weights for different vote types
        vneg_weight = -2
        neg_weight = -1
        pos_weight = 1
        vpos_weight = 2

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

        if requested_user_id:
            profile = get_user_model().objects.get(id=requested_user_id).profile
            scores_sum = (
                1
                if self.author.profile
                in profile.following.all().values_list("id", flat=True)
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
            rank = votes_total**2 + scores_sum + favorite + gravity / time_ago
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

    def dict_with_score(self, requested_user_id=None):
        data = {
            "id": self.id,
            "thread_id": self.thread.id,
            "type": self.c_type,
            "title": self.title,
            "body": self.body,
            "author": {
                "username": self.author.username,
                "profile_image": self.author.profile.profile_image_url,
                "profile_image_thumb_url": self.author.profile.profile_image_thumb_url,
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
        if requested_user_id:
            data["score"] = self.score(requested_user_id)

        return data


class CiviLink(models.Model):
    """Extend the existing model to support a graph structure
     (i.e., Problem -> Causes -> Problem -> solved_by -> Solution),


    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    RELATION_TYPE_CHOICES = (
        ('causes', 'Causes'),
        ('solves', 'Solves'),
        ('related', 'Related'),  # Optional, for general relationships
    )

    from_civi = models.ForeignKey(Civi, on_delete=models.CASCADE, related_name='outgoing_links')
    to_civi = models.ForeignKey(Civi, on_delete=models.CASCADE, related_name='incoming_links')
    relation_type = models.CharField(max_length=50, choices=RELATION_TYPE_CHOICES)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_civi.title} {self.get_relation_type_display()} {self.to_civi.title}"

    def __edge__(self) -> Tuple[list, Dict[str, str]]:
        """
        Documentation:
        Add to a graph like this:
        ```python
        import networkx as nx
        G = nx.DiGraph()
        a_link = CiviLink.objects.first()
        edge_args, edge_kwargs = a_link.__edge__()
        G.add_edge(*edge_args, **edge_kwargs)
        ```

        Returns:
            Tuple[list, Dict[str, str]]: the first is the args, the second the kwargs to the nx graph `add_edge` function
        """
        # link.from_civi.id, link.to_civi.id, relation=link.relation_type
        edge_kwargs = {
            "relation":self.relation_type
        }
        edge_args = [self.from_civi.id, self.to_civi.id]
        return edge_args, edge_kwargs




class Response(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        default=None,
        null=True,
        on_delete=models.PROTECT,
        related_name="responses",
    )
    civi = models.ForeignKey(
        Civi,
        default=None,
        null=True,
        on_delete=models.PROTECT,
        related_name="responses",
    )

    title = models.CharField(max_length=127)
    body = models.TextField(max_length=2047)

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
    civi = models.ForeignKey(
        Civi,
        related_name="images",
        on_delete=models.PROTECT,
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(
        upload_to=PathAndRename("civi_uploads"), null=True, blank=True
    )
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
    user = models.ForeignKey(
        get_user_model(),
        default=None,
        null=True,
        on_delete=models.PROTECT,
        related_name="activities",
    )
    thread = models.ForeignKey(
        Thread,
        default=None,
        null=True,
        on_delete=models.PROTECT,
        related_name="activities",
    )
    civi = models.ForeignKey(
        Civi,
        default=None,
        null=True,
        on_delete=models.PROTECT,
        related_name="activities",
    )

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

    class Meta:
        verbose_name_plural = "Activities"


class Rebuttal(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        default=None,
        null=True,
        on_delete=models.PROTECT,
        related_name="rebuttals",
    )
    response = models.ForeignKey(
        Response,
        default=None,
        null=True,
        on_delete=models.PROTECT,
        related_name="rebuttals",
    )

    body = models.TextField(max_length=1023)

    votes_vneg = models.IntegerField(default=0)
    votes_neg = models.IntegerField(default=0)
    votes_neutral = models.IntegerField(default=0)
    votes_pos = models.IntegerField(default=0)
    votes_vpos = models.IntegerField(default=0)
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

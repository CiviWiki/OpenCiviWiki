from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible
from django.core.files.storage import default_storage
from django.db import models
from django.conf import settings
from hashtag import Hashtag
from category import Category

import os, json, uuid

class AccountManager(models.Manager):
    def summarize(self, account):
        from civi import Civi
        data = {
            "username": account.user.username,
            "first_name": account.first_name,
            "last_name": account.last_name,
            "about_me": account.about_me,
            "location": account.get_location(),
            "history": [Civi.objects.serialize(c) for c in Civi.objects.filter(author_id=account.id).order_by('-created')],
            "profile_image": account.profile_image_url,
            "followers": self.followers(account),
            "following": self.following(account),
        }
        return data

    def chip_summarize(self, account):
        data = {
            "username": account.user.username,
            "first_name": account.first_name,
            "last_name": account.last_name,
            "profile_image": account.profile_image_url,
        }
        return data

    def card_summarize(self, account, request_account):
        data = {
            "id": account.user.id,
            "username": account.user.username,
            "first_name": account.first_name,
            "last_name": account.last_name,
            "about_me": account.about_me[:150] + ('' if len(account.about_me) <= 150 else '...'),
            "location": account.get_location(),
            "profile_image": account.profile_image_url,
            "follow_state": True if account in request_account.following.all() else False,
            "request_account": request_account.first_name
        }
        return data


    def followers(self, account):
        return [self.chip_summarize(a) for a in account.followers.all()]

    def following(self, account):
        return [self.chip_summarize(a) for a in account.following.all()]

@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        new_filename = str(uuid.uuid4())
        filename = '{}.{}'.format(new_filename, ext)
        return os.path.join(self.sub_path, filename)

profile_upload_path = PathAndRename('')


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=63, blank=False)
    last_name = models.CharField(max_length=63, blank=False)
    about_me = models.CharField(max_length=511, blank=True)

    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=False, default=0)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=False, default=0)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=63, blank=True)
    state = models.CharField(max_length=2, choices=settings.US_STATES, blank=True)
    zip_code = models.CharField(max_length=6, null=True)

    fed_district = models.CharField(max_length=63, default=None, null=True)
    state_district = models.CharField(max_length=63, default=None, null=True)

    categories = models.ManyToManyField(Category, related_name='user_categories', symmetrical=False)
    interests = models.ManyToManyField(Hashtag, related_name='interests')
    ai_interests = models.ManyToManyField(Hashtag, related_name='ai_interests')

    followers = models.ManyToManyField('self', related_name='follower', symmetrical=False)
    following = models.ManyToManyField('self', related_name='followings', symmetrical=False)

    beta_access = models.BooleanField(default=False)
    full_account = models.BooleanField(default=False)

    objects = AccountManager()
    profile_image = models.ImageField(upload_to=profile_upload_path, blank=True, null=True)

    #custom "row-level" functionality (properties) for account models
    def get_location(self):
        if self.city and self.state:
            return '{city}, {state}'.format(city=self.city, state=dict(settings.US_STATES).get(self.state))
        elif self.state:
            return '{state}'.format(state=dict(settings.US_STATES).get(self.state))
        else:
            return 'NO LOCATION'

    def _get_full_name(self):
        "Returns the person's full name."
        return '{first_name} {last_name}'.format(first_name=self.first_name, last_name=self.last_name)
    full_name = property(_get_full_name)

    def _get_profile_image_url(self):
        if self.profile_image and default_storage.exists(os.path.join(settings.MEDIA_ROOT, self.profile_image.name)):
            return self.profile_image.url
        else:
            #NOTE: This default url will probably be changed later
            return "/static/img/no_image_md.png",
    profile_image_url = property(_get_profile_image_url)

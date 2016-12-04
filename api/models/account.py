from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

import json
import os

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
            "profile_image": account.profile_image.url,
            "followers": self.followers(account),
            "following": self.following(account),
        }
        return data
    #
    def follow_summarize(self, account):
        data = {
            "username": account.user.username,
            "first_name": account.first_name,
            "last_name": account.last_name,
            "about_me": account.about_me,
            "location": account.get_location(),
            "profile_image": account.profile_image.url,
        }
        return json.dumps(data)


    def followers(self, account):
        return [self.follow_summarize(a) for a in account.followers.all()]

    def following(self, account):
        return [self.follow_summarize(a) for a in account.following.all()]

def path_and_rename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(instance.user.username, ext)
        return os.path.join(path, filename)
    return wrapper

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
    interests = models.ManyToManyField('Hashtag', related_name='interests')
    ai_interests = models.ManyToManyField('Hashtag', related_name='ai_interests')
    issues = models.ManyToManyField('Thread', related_name='issues')
    followers = models.ManyToManyField('self', related_name='follower')
    following = models.ManyToManyField('self', related_name='followings')

    beta_access = models.BooleanField(default=False)
    full_account = models.BooleanField(default=False)

    objects = AccountManager()
    #custom "row-level" functionality (properties) for account models

    def get_location(self):
        return '{city}, {state}'.format(city=self.city, state=dict(settings.US_STATES).get(self.state))

    def get_full_name(self):
        "Returns the person's full name."
        return '{first_name} {last_name}'.format(first_name=self.first_name, last_name=self.last_name)

    profile_image = models.ImageField(upload_to=path_and_rename('profile/'), blank=True, null=True, default ='profile/happy.png')

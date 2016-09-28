from django.contrib.auth.models import User
from django.db import models
import json
import os
# from django.contrib.postgres.fields import ArrayField

#TODO: email field needs to be removed (already in auth.User model)
#TODO: account manager needs ot be changed accordingly

class AccountManager(models.Manager):
    def summarize(self, account):
        from civi import Civi
        return {
            "username": account.user.username,
            "first_name": account.first_name,
            "last_name": account.last_name,
            "about_me": account.about_me,
            "zip_code": account.zip_code,
            "id": account.id,
            "history": [Civi.objects.serialize(c) for c in Civi.objects.filter(author_id=account.id).order_by('-created')],
            "profile_image": account.profile_image.url,
            "followers": [self.follow_summarize(a) for a in account.followers.all()],
            "following": [self.follow_summarize(a) for a in account.following.all()],
        }

    def follow_summarize(self, account):
        data = {
            "username": account.user.username,
            "first_name": account.first_name,
            "last_name": account.last_name,
            "about_me": account.about_me,
            "zip_code": account.zip_code,
            "id": account.id,
            "profile_image": account.profile_image.url,
        }
        return json.dumps(data)


    def serialize(self, account, filter=None):
        from civi import Civi
        data = {
            "username": account.user.username,
            "first_name": account.first_name,
            "last_name": account.last_name,
            "email": account.email,
            "last_login": str(account.last_login),
            "about_me": account.about_me,
            "valid": account.valid,
            "statistics": account.statistics,
            "interests": account.interests,
            "pins": [Civi.objects.summarize(c) for c in Civi.objects.filter(pk__in=account.civi_pins)],
            "history": [Civi.objects.serialize(c) for c in Civi.objects.filter(author_id=account.id).order_by('-created')],
            "friend_requests": [self.summarize(a) for a in self.filter(pk__in=account.friend_requests)],
            "zip_code": account.zip_code,
            "state": account.state,
            "city": account.city,
            "country": account.country,
            "address1": account.address1,
            "address2": account.address2,
            "friends": [self.summarize(a) for a in account.friends.all()]
        }
        if filter and filter in data:
            return {filter: data[filter]}
        return data

    def friends(self, account):
        friends = [self.summarize(a) for a in account.friends.all()]
        requests = [self.summarize(a) for a in self.filter(pk__in=account.friend_requests)]
        return dict(friends=friends, requests=requests)

def get_profile_path(account, filename):
    return os.path.join('profile', user_directory_path(account,filename))

def user_directory_path(account, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(account.user.id, filename)


class Account(models.Model):
    objects = AccountManager()

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=63, blank=False)
    last_name = models.CharField(max_length=63, blank=False)
    email = models.CharField(max_length=63, unique=True, blank=False)
    about_me = models.CharField(max_length=511, blank=True)

    zip_code = models.CharField(max_length=10, blank=True)
    state = models.CharField(max_length=63, blank=True)

    fed_district = models.CharField(max_length=63, default=None, null=True)
    state_district = models.CharField(max_length=63, default=None, null=True)

    profile_image = models.ImageField(upload_to=get_profile_path, blank=True, null=True)

    beta_access = models.BooleanField(default=False)

    interests = models.ManyToManyField('Hashtag', related_name='interests')
    ai_interests = models.ManyToManyField('Hashtag', related_name='ai_interests')

    followers = models.ManyToManyField('self', related_name='follower')
    following = models.ManyToManyField('self', related_name='following')

    issues = models.ManyToManyField('Thread', related_name='issues')

from django.contrib.auth.models import User
from django.db import models
from hashtag import Hashtag
# from django.contrib.postgres.fields import ArrayField


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
            "history": [Civi.objects.serialize(c) for c in Civi.objects.filter(author_id=account.id).order_by('-created')]
        }

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
            "cover_image": account.cover_image,
            "statistics": account.statistics,
            "interests": account.interests,
            "pins": [Civi.objects.summarize(c) for c in Civi.objects.filter(pk__in=account.civi_pins)],
            "history": [Civi.objects.serialize(c) for c in Civi.objects.filter(author_id=account.id).order_by('-created')],
            "friend_requests": [self.summarize(a) for a in self.filter(pk__in=account.friend_requests)],
            "zip_code": account.zip_code,
            "country": account.country,
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

    # profile_image = models.CharField(max_length=255)

    beta_access = models.BooleanField(default=False)

    interests = models.ManyToManyField(Hashtag, related_name='interests')
    ai_interests = models.ManyToManyField(Hashtag, related_name='ai_interests')

    followers = models.ManyToManyField('self', related_name='follower')
    following = models.ManyToManyField('self', related_name='following')

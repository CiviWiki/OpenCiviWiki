from __future__ import unicode_literals
from django.db import models
import json
import datetime
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from group import Group
from civi import Civi

class AccountManager(models.Manager):

    def summarize(self, account):

        return {
            "first_name": account.first_name,
            "last_name": account.last_name,
            "profile_image": account.profile_image,
            "id": account.id
        }

    def serialize(self, account, filter=None):

        data = {
            "username": account.user.username,
            "first_name": account.first_name,
            "last_name": account.last_name,
            "email": account.email,
            "last_login": str(account.last_login),
            "about_me": account.about_me,
            "valid": account.valid,
            "profile_image": account.profile_image,
            "cover_image": account.cover_image,
            "statistics": account.statistics,
            "interests": account.interests,
            "pins": [Civi.objects.summarize(c) for c in Civi.objects.filter(pk__in=account.civi_pins)],
            "history": [Civi.objects.summarize(c) for c in Civi.objects.filter(pk__in=account.civi_history)],
            "friend_requests": [self.summarize(a) for a in self.filter(pk__in=account.friend_requests)],
            "awards": [award for a in account.award_list],
            "zip_code": account.zip_code,
            "country": account.country,
            "state": account.state,
            "city": account.city,
            "country": account.country,
            "address1": account.address1,
            "address2": account.address2,
            "groups": [Group.objects.summarize(g) for g in account.groups.all()],
            "friends": [self.summarize(a) for a in account.friends.all()]
        }
        if filter and filter in data:
            return {filter: data[filter]}
        return data

    def retrieve(self, user):
        return self.find(user=user)[0]

class Account(models.Model):
    '''
    Holds meta information about an Account, not used to login.
    '''
    objects = AccountManager()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=63, blank=False)
    last_name = models.CharField(max_length=63, blank=False)
    email = models.CharField(max_length=63, unique=True, blank=False)
    last_login = models.DateTimeField(auto_now=True)
    about_me = models.CharField(max_length=511, blank=True)
    valid = models.BooleanField(default=False)
    profile_image = models.CharField(max_length=255)
    cover_image = models.CharField(max_length=255)
    statistics = models.TextField(blank=True)
    interests = ArrayField(models.CharField(max_length=127, blank=True), default=[], blank=True)
    civi_pins = ArrayField(models.CharField(max_length=127, blank=True), default=[], blank=True)
    civi_history = ArrayField(models.CharField(max_length=127, blank=True), size=10, default=[], blank=True)
    friend_requests = ArrayField(models.CharField(max_length=127, blank=True), default=[], blank=True)
    award_list = ArrayField(models.CharField(max_length=127, blank=True), default=[], blank=True)
    zip_code = models.CharField(max_length=6, blank=True)
    country = models.CharField(max_length=46, blank=True)
    state = models.CharField(max_length=63, blank=True)
    city = models.CharField(max_length=63, blank=True)
    address1 = models.CharField(max_length=255, blank=True)
    address2 = models.CharField(max_length=255, blank=True)
    groups = models.ManyToManyField('Group', related_name='user_groups')
    friends = models.ManyToManyField('Account', related_name='friended_account')

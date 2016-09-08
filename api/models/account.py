from django.contrib.auth.models import User
from django.db import models
from hashtag import Hashtag
# from django.contrib.postgres.fields import ArrayField


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=63, blank=False)
    last_name = models.CharField(max_length=63, blank=False)
    email = models.CharField(max_length=63, unique=True, blank=False)
    about_me = models.CharField(max_length=511, blank=True)

    zip_code = models.CharField(max_length=10, blank=True)
    state = models.CharField(max_length=63, blank=True)

    fed_district = models.CharField(max_length=63)
    state_district = models.CharField(max_length=63)

    # profile_image = models.CharField(max_length=255)

    beta_access = models.BooleanField(default=False)

    interests = models.ManyToManyField(Hashtag)
    ai_interests = models.ManyToManyField(Hashtag)

    followers = models.ManyToManyField('self', related_name='follower')
    following = models.ManyToManyField('self', related_name='following')

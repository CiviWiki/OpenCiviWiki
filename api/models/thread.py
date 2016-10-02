from django.db import models
from account import Account
from category import Category
from fact import Fact
from hashtag import Hashtag
from topic import Topic


class Thread(models.Model):
    author = models.ForeignKey(Account, default=None, null=True)
    category = models.ForeignKey(Category, default=None, null=True)
    topic = models.ForeignKey(Topic, default=None, null=True)
    facts = models.ManyToManyField(Fact)

    hashtags = models.ManyToManyField(Hashtag)

    title = models.CharField(max_length=63)
    summary = models.CharField(max_length=4095)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

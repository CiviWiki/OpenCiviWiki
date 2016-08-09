from __future__ import unicode_literals
from django.db import models
from account import Account
from civi import Civi, Response
from django.contrib.postgres.fields import ArrayField
import json

class ThreadManager(models.Manager):
    def serialize(self, thread):
        pass

class Thread(models.Model):
    objects = ThreadManager();
    title = models.CharField(max_length=63)
    summary = models.CharField(max_length=4095)

    facts = ArrayField(models.CharField(max_length=1023, blank=True), default=[], blank=True)
    contributors = models.ManyToManyField(Account)
    category = models.ForeignKey('Category', default=None, null=True)
    topic = models.ForeignKey('Topic', default=None, null=True)

    problem = models.ManyToManyField(Civi, related_name='problem')
    cause = models.ManyToManyField(Civi, related_name='cause')
    solution = models.ManyToManyField(Civi, related_name='solution')

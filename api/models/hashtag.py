from __future__ import unicode_literals
from django.db import models
import json

class HashtagManager(models.Manager):

    def summarize(self, hashtag):
        return {
            "title": hashtag.title
        }
        
    def serialize(self, hashtag):
        data ={
             "title": hashtag.title,
             "votes_n1": hashtag.votes_negative1,
             "votes_n2": hashtag.votes_negative2,
             "votes_neutral": hashtag.votes_neutral,
             "votes_p1": hashtag.votes_positive1,
             "votes_p2": hashtag.votes_positive2
        }
        return json.dumps(data)

class Hashtag(models.Model):
    '''
    Hashtags store the civis that they appear in, their text,
    and the vote distribution of the civis they appear in.
    '''
    objects = HashtagManager()
    title = models.CharField(max_length=63, default='')
    votes_negative2 = models.IntegerField(default=0, null=True)
    votes_negative1 = models.IntegerField(default=0, null=True)
    votes_neutral = models.IntegerField(default=0, null=True)
    votes_positive1 = models.IntegerField(default=0, null=True)
    votes_positive2 = models.IntegerField(default=0, null=True)

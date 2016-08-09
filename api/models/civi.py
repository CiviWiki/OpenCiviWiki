from __future__ import unicode_literals
from django.db import models
from hashtag import Hashtag
from django.contrib.postgres.fields import ArrayField
from operator import itemgetter
import math, json

class CiviManager(models.Manager):
    def summarize(self, civi):
        return {
            "id": civi.id,
            "title": civi.title,
            "body": civi.body[0:150]
        }

    def serialize(self, civi, filter=None):
        from account import Account
        data = {
            "title": civi.title,
            "body": civi.body,
            "group": Account.objects.summarize(civi.group),
            "creator": Account.objects.summarize(civi.creator),
            "visits": civi.visits,
            "topic": civi.topic,
            "hashtags": [h.title for h in civi.hashtags.all()],
            "type": civi.type,
            "id": civi.id,
            "REF": civi.reference_id,
	    }

        if filter and filter in data:
            return json.dumps({filter: data[filter]})
        return json.dumps(data)

    def calcPolarity(self, civi):
        '''
            polarity : ( positive2 / visits ) + ( .5 * positive / visits ) + (.5 * negative / visits ) + ( negative2 / visits )
            polarity takes a value between 0 and 1, approaching 0 as votes cluster around neutral, and approach one as votes
            cluster amoung stronger alignments.

        '''
        polarity = ( civi.votes_positive2 + civi.votes_negative1 + .5 * ( civi.votes_positive1 + civi.votes_negative2 ) )
        polarity /= civi.visits
        return polarity


    def aveVote(self, civi):
        '''
            average vote ranges between 0 and 5. Scaled like this so it can be used as a direct multiplier for score and ignore votes with heavily negative weights.
        '''
        ave = -1 * ( civi.votes_negative1 + 2 * civi.votes_negative2 ) + ( 2 * civi.votes_positive2 + civi.votes_positive1 )
        ave /= civi.visits
        return ave + 5

    def aveScore(self, civi):
        '''
            Average score is a summation of the vote values recieved,
            - moved onto a logarithmic scale
            - lastly scaled by amplifier to allow an integer effect by the Polarity.
        '''
        score = -1 * ( civi.votes_negative1 + 2 * civi.votes_negative2 ) + ( 2 * civi.votes_positive2 + civi.votes_positive1 )
        log_shift = math.log(civi.visits)
        amplifier = math.pow(10,10)

        return score * log_shift * amplifier

    def getChain(self, id_list):
        if len(id_list):
            return [self.serialize(self.get(id)) for id in id_list]
        return  []

    def block(self, topic, start=0, end=0):
        '''
            Scores Civis and sorts them returning the block.
            TODO: this may get slow in the long run. Maybe we should keep a score on every civi that is updated when a civi is
            voted on?
        '''
        def score(c):
            return int(c.aveScore() * c.calcPolarity())

        if end == 0:
            end = start + 10
        id_and_score = [{'id':c.id, 'score': score(c)} for c in self.filter(topic=topic, type='I')]
        id_and_score = sorted(id_and_score, key=itemgetter('score'), reverse=True )[start:end]

        ids = [a['id'] for a in id_and_score]
        return [self.summarize(civi) for civi in self.filter(id__in=ids)]

class Response(models.Model):
    objects = CiviManager()
    creator = models.ForeignKey('Account', default=None, null=True)

    title = models.CharField(max_length=63)
    body = models.TextField(max_length=4095)
    sources = ArrayField(models.CharField(max_length=127, blank=True), default=[], blank=True)

    votes_negative2 = models.IntegerField(default=0)
    votes_negative1 = models.IntegerField(default=0)
    votes_neutral = models.IntegerField(default=0)
    votes_positive1 = models.IntegerField(default=0)
    votes_positive2 = models.IntegerField(default=0)

class Civi(models.Model):
    objects = CiviManager()
    creator = models.ForeignKey('Account', default=None, null=True)
    thread = models.ForeignKey('Thread', default=None, null=True)
    response = models.ManyToManyField(Response)

    hashtags = models.ManyToManyField(Hashtag)

    title = models.CharField(max_length=63)
    body = models.TextField(max_length=4095)
    sources = ArrayField(models.CharField(max_length=127, blank=True), default=[], blank=True)

    votes_negative2 = models.IntegerField(default=0)
    votes_negative1 = models.IntegerField(default=0)
    votes_neutral = models.IntegerField(default=0)
    votes_positive1 = models.IntegerField(default=0)
    votes_positive2 = models.IntegerField(default=0)

    visits = models.IntegerField(default=0)

    bill_source = models.CharField(max_length=127, default=None, null=True)
    bill_for = models.IntegerField(default=0, null=True)
    bill_against = models.IntegerField(default=0, null=True)

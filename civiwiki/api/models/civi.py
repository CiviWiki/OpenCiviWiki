from __future__ import unicode_literals
from django.db import models
from hashtag import Hashtag
# from group import Group
from django.contrib.postgres.fields import ArrayField
from operator import itemgetter
import math, json

class CiviManager(models.Manager):
    def summarize(self, civi):
        return {
            "id": civi.id,
            "title": civi.title,
            # "group": Group.objects.summarize(civi.group),
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
            #"AT": getChain(civi.at_id),
            #"AND_NEGATIVE": getChain(civi.and_negative_id),
            #"AND_POSITIVE": getChain(civi.and_positive_id)
	    }

        if filter and filter in data:
            return json.dumps({filter: data[filter]})
        return json.dumps(data)

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

class Civi(models.Model):
    '''
    This is the model schema for the primary object in
    the application. Hold an id field and does not hold
    references to other objects. Maybe not the fastest
    implementation but it simplifies things such as searching.
    '''
    objects = CiviManager()
    group = models.ForeignKey('Group', default=None, null=True)
    creator = models.ForeignKey('Account', default=None, null=True)
    category = models.ForeignKey('Category', default=None, null=True)
    topic = models.ForeignKey('Topic', default=None, null=True)
    hashtags = models.ManyToManyField(Hashtag)

    title = models.CharField(max_length=63)
    body = models.TextField(max_length=4095)

    votes_negative2 = models.IntegerField(default=0)
    votes_negative1 = models.IntegerField(default=0)
    votes_neutral = models.IntegerField(default=0)
    votes_positive1 = models.IntegerField(default=0)
    votes_positive2 = models.IntegerField(default=0)

    visits = models.IntegerField(default=0)
    type = models.CharField(max_length=2, default='I')#Possible values of I, C, or S for
    #issue, cause, and solution
    reference = ArrayField(models.CharField(max_length=127, blank=True), default=[], blank=True)
    at = ArrayField(models.CharField(max_length=127, blank=True), default=[], blank=True)
    and_negative = ArrayField(models.CharField(max_length=127, blank=True), default=[], blank=True)
    and_positive = ArrayField(models.CharField(max_length=127, blank=True), default=[], blank=True)


    NEG2_WEIGHT = 2
    NEG1_WEIGHT = 1
    NEUTRAL_WEIGHT = 0
    POS1_WEIGHT = 1
    POS2_WEIGHT = 2
    SCALE_POLARITY = 2

    RANK_CUTOFF = -1

    def calcPolarity(self):
        '''
            polarity : ( positive2 / visits ) + ( .5 * positive / visits ) + (.5 * negative / visits ) + ( negative2 / visits )
            polarity takes a value between 0 and 1, approaching 0 as votes cluster around neutral, and approach one as votes
            cluster amoung stronger alignments.

        '''
        polarity = ( self.votes_positive2 + self.votes_negative1 + .5 * ( self.votes_positive1 + self.votes_negative2 ) )
        polarity /= self.visits
        return polarity


    def aveVote(self):
        '''
            average vote ranges between 0 and 5. Scaled like this so it can be used as a direct multiplier for score and ignore votes with heavily negative weights.
        '''
        ave = -1 * ( self.votes_negative1 + 2 * self.votes_negative2 ) + ( 2 * self.votes_positive2 + self.votes_positive1 )
        ave /= self.visits
        return ave + 5

    def aveScore(self):
        '''
            Average score is a summation of the vote values recieved,
            - moved onto a logarithmic scale
            - lastly scaled by amplifier to allow an integer effect by the Polarity.
        '''
        score = -1 * ( self.votes_negative1 + 2 * self.votes_negative2 ) + ( 2 * self.votes_positive2 + self.votes_positive1 )
        log_shift = math.log(self.visits)
        amplifier = math.pow(10,10)

        return score * log_shift * amplifier

from __future__ import unicode_literals
from django.db import models
import json
from category import Category
class TopicManager(models.Manager):
   def serialize(self, topic):
      data ={
         "category": Category.objects.summarize(topic.category),
         "topic": topic.topic,
         "bill": topic.bill,
      }
      return json.dumps(data)

class Topic(models.Model):
    objects = TopicManager()
    category = models.ForeignKey('Category')
    topic = models.CharField(max_length=63)
    bill = models.URLField(null=True)

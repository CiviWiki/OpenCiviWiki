from __future__ import unicode_literals
from django.db import models
import json

class CategoryManager(models.Manager):
   def summarize(self, category):
      return {
         "name": category.name,
      }

   def serialize(self, category):
      data ={
         "name": category.name,
      }
      return json.dumps(data)

class Category(models.Model):
    '''
    Category holds all topics of a similar genre
    '''
    objects = CategoryManager()
    name = models.CharField(max_length=63)

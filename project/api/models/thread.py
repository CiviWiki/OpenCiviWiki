from django.db import models
from account import Account
from category import Category
from fact import Fact
from hashtag import Hashtag
from calendar import month_name
import os, json, uuid
from django.utils.deconstruct import deconstructible
from django.core.files.storage import default_storage
from django.conf import settings
from utils.constants import US_STATES

class ThreadManager(models.Manager):
    #TODO: move this to read.py, try to be more query operation specific here
    def summarize(self, thread):
        # Number of characters after which to truncate thread
        thread_truncate_length = 320

        # If thread length is longer than truncate length... add elipsis (truncate)
        ellipsis_if_too_long = '' if len(thread.summary) <= thread_truncate_length else '...'

        from civi import Civi
        thread_data = {
            "id": thread.id,
            "title": thread.title,
            "summary": thread.summary[:thread_truncate_length] + (ellipsis_if_too_long),
            "created": "{0} {1}, {2}".format(month_name[thread.created.month], thread.created.day, thread.created.year),
            "category_id": thread.category.id,
            "image": thread.image_url
        }
        author_data = {
            "username": thread.author.user.username,
            "full_name": thread.author.full_name,
            "profile_image": thread.author.profile_image_url
        }
        stats_data = {
            "num_views": thread.num_views,
            "num_civis": Civi.objects.all().filter(thread_id=thread.id).count(), # thread.num_civis,
            "num_solutions": thread.num_solutions
        }

        data = {
            "thread": thread_data,
            "author": author_data,
            "stats": stats_data
        }
        return data

    def filter_by_category(self, categories):
        return self.all().filter(category__in=categories)

@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        extension = filename.split('.')[-1]
        new_filename = str(uuid.uuid4())
        filename = '{}.{}'.format(new_filename, extension)
        return os.path.join(self.sub_path, filename)

image_upload_path = PathAndRename('')

class Thread(models.Model):
    author = models.ForeignKey(Account, default=None, null=True)
    category = models.ForeignKey(Category, default=None, null=True)
    facts = models.ManyToManyField(Fact)

    hashtags = models.ManyToManyField(Hashtag)

    title = models.CharField(max_length=127, blank=False, null=False)
    summary = models.CharField(max_length=4095, blank=False, null=False)
    image = models.ImageField(upload_to=image_upload_path, blank=True, null=True)

    level_CHOICES = (
        ('federal', 'Federal'),
        ('state', 'State'),
    )
    level = models.CharField(max_length=31, default='federal', choices=level_CHOICES)
    state = models.CharField(max_length=2, choices=US_STATES, blank=True)

    def _get_image_url(self): #TODO: move this to utils
        if self.image and default_storage.exists(os.path.join(settings.MEDIA_ROOT, self.image.name)):
            return self.image.url
        else:
            #NOTE: This default url will probably be changed later
            return "/static/img/no_image_md.png"

    image_url = property(_get_image_url)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    num_views = models.IntegerField(default=0)
    num_civis = models.IntegerField(default=0)
    num_solutions = models.IntegerField(default=0)

    objects = ThreadManager()

    def _get_created_date_str(self):
        d = self.created
        return "{0} {1}, {2}".format(month_name[d.month], d.day, d.year)
        
    created_date_str = property(_get_created_date_str)

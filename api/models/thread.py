from django.db import models
from account import Account
from category import Category
from fact import Fact
from hashtag import Hashtag
from calendar import month_name

class ThreadManager(models.Manager):
    #TODO: move this to read.py, try to be more query operation specific here
    def summarize(self, thread):
        from civi import Civi
        thread_data = {
            "id": thread.id,
            "title": thread.title,
            "summary": thread.summary, #thread.summary[:320] + ('' if len(thread.summary) <= 320 else '...'),
            "created": "{0} {1}, {2}".format(month_name[thread.created.month], thread.created.day, thread.created.year),
            "category_id": thread.category.id
        }
        author_data = {
            "username": thread.author.user.username,
            "full_name": thread.author.get_full_name(),
            "profile_image": thread.author.profile_image.url if thread.author.profile_image else "/media/profile/default.png"
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

class Thread(models.Model):
    author = models.ForeignKey(Account, default=None, null=True)
    category = models.ForeignKey(Category, default=None, null=True)
    facts = models.ManyToManyField(Fact)

    hashtags = models.ManyToManyField(Hashtag)

    title = models.CharField(max_length=127, blank=False, null=False)
    summary = models.CharField(max_length=4095, blank=False, null=False)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    num_views = models.IntegerField(default=0)
    num_civis = models.IntegerField(default=0)
    num_solutions = models.IntegerField(default=0)

    objects = ThreadManager()

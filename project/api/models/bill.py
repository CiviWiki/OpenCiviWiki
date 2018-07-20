from django.db import models


class Bill(models.Model):
    """
    The bill class converts a text post, such as a bill stub, into a db entry
    """
    
    #id is the unique identifier for each db entry
    id = models.CharField(max_length=255, primary_key=True)

    title = models.CharField(max_length=1023)
    short_title = models.CharField(max_length=1023)
    short_summary = models.CharField(max_length=1023)
    number = models.IntegerField(default=0)
    b_type = models.CharField(max_length=63)

    # status
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

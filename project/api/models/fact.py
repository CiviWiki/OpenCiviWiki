from django.db import models

class Fact(models.Model):
    """
    Provides the body, created, and last_modified date/time for a model.
    """
    body = models.CharField(max_length=511)
    
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

from django.db import models

class Fact(models.Model):
    body = models.CharField(max_length=511)
    
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

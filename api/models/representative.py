from django.db import models
from account import Account


class Representative(models.Model):
    account = models.ForeignKey(Account, default=None, null=True)

    district = models.CharField(max_length=63) # junior or senior for senator
    state = models.CharField(max_length=63)

    level_CHOICES = (
        ('federal', 'Federal'),
        ('state', 'State'),
    )
    level = models.CharField(max_length=31, default='federal', choices=level_CHOICES)

    term_start = models.DateField()
    term_end = models.DateField()

    party = models.CharField(max_length=127)

    bioguideID = models.CharField(max_length=7, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

from django.db import models

from .bill import Bill
from .representative import Representative


class Vote(models.Model):
    bill = models.ForeignKey(Bill, default=None, null=True)
    representative = models.ForeignKey(Representative, default=None, null=True)

    vote_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No'),
        ('abstain', 'Abstain'),
    )
    vote = models.CharField(max_length=31, default='abstain', choices=vote_CHOICES)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)

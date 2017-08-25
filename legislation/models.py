from django.db import models

# Create your models here.
class Bill(models.Model):
    identifier = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500)

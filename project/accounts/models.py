from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    A new custom User model for any functionality needed in the future. Extending AbstractUser
    allows for adding new fields to the user model as needed.
    """
    class Meta:
        db_table = 'users'

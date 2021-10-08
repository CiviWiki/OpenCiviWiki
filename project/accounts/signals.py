from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from accounts.models import Profile


@receiver(post_save, sender=get_user_model())
def create_related_profile(sender, instance, created, *args, **kwargs):
    """
    Only when a `User` instance is created, create a `Profile` instance.
    If a `User` instance is updated, do not create a `Profile` instance.
    """
    if instance and created:
        instance.profile = Profile.objects.create(user=instance)

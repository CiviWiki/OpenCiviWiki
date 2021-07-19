"""
Account Model
Extends the default django user model
"""

import os
import uuid
import io

from django.utils.deconstruct import deconstructible
from django.core.files.storage import default_storage
from django.conf import settings
from django.db import models
from PIL import Image, ImageOps
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth import get_user_model

from core.constants import US_STATES
from taggit.managers import TaggableManager
from .category import Category

# Image manipulation constants
PROFILE_IMG_SIZE = (171, 171)
PROFILE_IMG_THUMB_SIZE = (40, 40)
WHITE_BG = (255, 255, 255)

# get custom user model
User = get_user_model()


class AccountManager(models.Manager):
    def summarize(self, account):
        from .civi import Civi

        data = {
            "username": account.user.username,
            "first_name": account.first_name,
            "last_name": account.last_name,
            "about_me": account.about_me,
            "history": [
                Civi.objects.serialize(c)
                for c in Civi.objects.filter(author_id=account.id).order_by("-created")
            ],
            "profile_image": account.profile_image_url,
            "followers": self.followers(account),
            "following": self.following(account),
        }
        return data

    def chip_summarize(self, account):
        data = {
            "username": account.user.username,
            "first_name": account.first_name,
            "last_name": account.last_name,
            "profile_image": account.profile_image_url,
        }
        return data

    def card_summarize(self, account, request_account):
        # Length at which to truncate 'about me' text
        about_me_truncate_length = 150

        # If 'about me' text is longer than 150 characters... add elipsis (truncate)
        ellipsis_if_too_long = (
            "" if len(account.about_me) <= about_me_truncate_length else "..."
        )

        data = {
            "id": account.user.id,
            "username": account.user.username,
            "first_name": account.first_name,
            "last_name": account.last_name,
            "about_me": account.about_me[:about_me_truncate_length]
            + (ellipsis_if_too_long),
            "profile_image": account.profile_image_url,
            "follow_state": True
            if account in request_account.following.all()
            else False,
            "request_account": request_account.first_name,
        }
        return data

    def followers(self, account):
        return [self.chip_summarize(follower) for follower in account.followers.all()]

    def following(self, account):
        return [self.chip_summarize(following) for following in account.following.all()]


@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        extension = filename.split(".")[-1]
        new_filename = str(uuid.uuid4())
        filename = "{}.{}".format(new_filename, extension)
        return os.path.join(self.sub_path, filename)


profile_upload_path = PathAndRename("")




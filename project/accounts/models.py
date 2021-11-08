from django.contrib.auth.models import AbstractUser
import os
import io
from django.core.files.storage import default_storage
from django.conf import settings
from django.db import models
from PIL import Image, ImageOps
from django.core.files.uploadedfile import InMemoryUploadedFile
from taggit.managers import TaggableManager

from categories.models import Category
from common.utils import PathAndRename


class User(AbstractUser):
    """
    A new custom User model for any functionality
    needed in the future. Extending AbstractUser
    allows for adding new fields to the user model as needed.
    """

    class Meta:
        db_table = "users"


# Image manipulation constants
PROFILE_IMG_SIZE = (171, 171)
PROFILE_IMG_THUMB_SIZE = (40, 40)
WHITE_BG = (255, 255, 255)


class ProfileManager(models.Manager):
    def summarize(self, profile):
        from threads.models import Civi

        data = {
            "username": profile.user.username,
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "about_me": profile.about_me,
            "history": [
                Civi.objects.serialize(c)
                for c in Civi.objects.filter(author_id=profile.id).order_by("-created")
            ],
            "profile_image": profile.profile_image_url,
            "followers": self.followers(profile),
            "following": self.following(profile),
        }
        return data

    def chip_summarize(self, profile):
        data = {
            "username": profile.user.username,
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "profile_image": profile.profile_image_url,
        }
        return data

    def card_summarize(self, profile, request_profile):
        # Length at which to truncate 'about me' text
        about_me_truncate_length = 150

        # If 'about me' text is longer than 150 characters... add elipsis (truncate)
        ellipsis_if_too_long = (
            "" if len(profile.about_me) <= about_me_truncate_length else "..."
        )

        data = {
            "id": profile.user.id,
            "username": profile.user.username,
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "about_me": profile.about_me[:about_me_truncate_length]
            + ellipsis_if_too_long,
            "profile_image": profile.profile_image_url,
            "follow_state": True
            if profile in request_profile.following.all()
            else False,
            "request_profile": request_profile.first_name,
        }
        return data

    def followers(self, profile):
        return [self.chip_summarize(follower) for follower in profile.followers.all()]

    def following(self, profile):
        return [self.chip_summarize(following) for following in profile.following.all()]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=63, blank=False)
    last_name = models.CharField(max_length=63, blank=False)
    about_me = models.CharField(max_length=511, blank=True)

    categories = models.ManyToManyField(
        Category, related_name="user_categories", symmetrical=False
    )
    tags = TaggableManager()

    followers = models.ManyToManyField(
        "self", related_name="follower", symmetrical=False
    )
    following = models.ManyToManyField(
        "self", related_name="followings", symmetrical=False
    )

    is_verified = models.BooleanField(default=False)
    full_profile = models.BooleanField(default=False)

    objects = ProfileManager()
    profile_image = models.ImageField(
        upload_to=PathAndRename("profile_uploads"), blank=True, null=True
    )
    profile_image_thumb = models.ImageField(
        upload_to=PathAndRename("profile_uploads"), blank=True, null=True
    )

    @property
    def full_name(self):
        """Returns the person's full name."""

        return f"{self.first_name} {self.last_name}"

    @property
    def profile_image_url(self):
        """Return placeholder profile image if user didn't upload one"""

        if self.profile_image:
            file_exists = default_storage.exists(
                os.path.join(settings.MEDIA_ROOT, self.profile_image.name)
            )
            if file_exists:
                return self.profile_image.url

        return "/static/img/no_image_md.png"

    @property
    def profile_image_thumb_url(self):
        """Return placeholder profile image if user didn't upload one"""

        if self.profile_image_thumb:
            file_exists = default_storage.exists(
                os.path.join(settings.MEDIA_ROOT, self.profile_image_thumb.name)
            )
            if file_exists:
                return self.profile_image_thumb.url

        return "/static/img/no_image_md.png"

    def __init__(self, *args, **kwargs):
        super(Profile, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Image crop/resize and thumbnail creation"""

        # New Profile image --
        if self.profile_image:
            self.resize_profile_image()

        self.full_profile = self.is_full_profile()

        super(Profile, self).save(*args, **kwargs)

    def resize_profile_image(self):
        """
        Resizes and crops the user uploaded image and creates a thumbnail version of it
        """
        profile_image = Image.open(self.profile_image)
        # Resize image
        profile_image = ImageOps.fit(
            profile_image, PROFILE_IMG_SIZE, Image.ANTIALIAS, centering=(0.5, 0.5)
        )

        # Convert to JPG image format with white background
        if profile_image.mode not in ("L", "RGB"):
            white_bg_img = Image.new("RGB", PROFILE_IMG_SIZE, WHITE_BG)
            white_bg_img.paste(profile_image, mask=profile_image.split()[3])
            profile_image = white_bg_img

        # Save new cropped image
        tmp_image_file = io.BytesIO()
        profile_image.save(tmp_image_file, "JPEG", quality=90)
        tmp_image_file.seek(0)
        self.profile_image = InMemoryUploadedFile(
            tmp_image_file,
            "ImageField",
            self.profile_image.name,
            "image/jpeg",
            profile_image.tell(),
            None,
        )
        # Make a Thumbnail Image for the new resized image
        thumb_image = profile_image.copy()

        thumb_image.thumbnail(PROFILE_IMG_THUMB_SIZE, resample=Image.ANTIALIAS)
        tmp_thumb_file = io.BytesIO()
        thumb_image.save(tmp_thumb_file, "JPEG", quality=90)
        tmp_thumb_file.seek(0)

        self.profile_image_thumb = InMemoryUploadedFile(
            tmp_thumb_file,
            "ImageField",
            self.profile_image.name,
            "image/jpeg",
            thumb_image.tell(),
            None,
        )

    def is_full_profile(self):
        if self.first_name and self.last_name:
            return True
        else:
            return False

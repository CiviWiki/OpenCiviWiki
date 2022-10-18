import io
import os

from categories.models import Category
from common.utils import PathAndRename
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from PIL import Image, ImageOps
from taggit.managers import TaggableManager


class User(AbstractUser):
    """
    A new custom User model for any functionality
    needed in the future. Extending AbstractUser
    allows for adding new fields to the user model as needed.
    """

    class Meta:
        db_table = "users"

    @property
    def upvoted_solutions(self):
        """
        Return solutions that this user has given a positive vote.
        """
        # Avoid circular dependencies
        from threads.models import Activity

        return Activity.objects.filter(
            user=self.id, civi__c_type="solution", activity_type__contains="pos"
        )

    def __str__(self) -> str:
        return self.username


# Image manipulation constants
PROFILE_IMG_SIZE = (171, 171)
PROFILE_IMG_THUMB_SIZE = (40, 40)
WHITE_BG = (255, 255, 255)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=63, blank=False)
    last_name = models.CharField(max_length=63, blank=False)
    about_me = models.CharField(max_length=511, blank=True)

    categories = models.ManyToManyField(
        Category, related_name="user_categories", symmetrical=False
    )
    tags = TaggableManager()

    following = models.ManyToManyField("self", related_name="followers")

    is_verified = models.BooleanField(default=False)

    profile_image = models.ImageField(
        upload_to=PathAndRename("profile_uploads"), blank=True, null=True
    )
    profile_image_thumb = models.ImageField(
        upload_to=PathAndRename("profile_uploads"), blank=True, null=True
    )

    def __str__(self):
        return f"{self.user.username} profile"

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

    def save(self, *args, **kwargs):
        """Image crop/resize and thumbnail creation"""

        # New Profile image --
        if self.profile_image:
            self.resize_profile_image()

        super(Profile, self).save(*args, **kwargs)

    def resize_profile_image(self):
        """
        Resizes and crops the user uploaded image and creates a thumbnail version of it
        """

        # TODO: try to remove this resize_profile_image method
        # or find a more simple way to acheive the goal(s)
        # - less disk space?
        # - desired shape?

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

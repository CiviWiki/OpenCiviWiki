from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    A new custom User model for any functionality needed in the future. Extending AbstractUser
    allows for adding new fields to the user model as needed.
    """
    class Meta:
        db_table = 'users'

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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

    beta_access = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    full_account = models.BooleanField(default=False)

    objects = AccountManager()
    profile_image = models.ImageField(
        upload_to=profile_upload_path, blank=True, null=True
    )
    profile_image_thumb = models.ImageField(
        upload_to=profile_upload_path, blank=True, null=True
    )

    @property
    def full_name(self):
        "Returns the person's full name."

        full_name = "{first_name} {last_name}".format(
            first_name=self.first_name, last_name=self.last_name
        )
        return full_name

    @property
    def profile_image_url(self):
        """ Return placeholder profile image if user didn't upload one"""

        if self.profile_image:
            file_exists = default_storage.exists(
                os.path.join(settings.MEDIA_ROOT, self.profile_image.name)
            )
            if file_exists:
                return self.profile_image.url

        return "/static/img/no_image_md.png"

    @property
    def profile_image_thumb_url(self):
        """ Return placeholder profile image if user didn't upload one"""

        if self.profile_image_thumb:
            file_exists = default_storage.exists(
                os.path.join(settings.MEDIA_ROOT, self.profile_image_thumb.name)
            )
            if file_exists:
                return self.profile_image_thumb.url

        return "/static/img/no_image_md.png"

    def __init__(self, *args, **kwargs):
        super(Account, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        """ Image crop/resize and thumbnail creation """

        # New Profile image --
        if self.profile_image:
            self.resize_profile_image()

        self.full_account = self.is_full_account()

        super(Account, self).save(*args, **kwargs)

    def resize_profile_image(self):
        """
        Resizes and crops the user uploaded image and creates a thumbnail version of it
        """
        profile_image_field = self.profile_image
        image_file = io.StringIO(profile_image_field.read())
        profile_image = Image.open(image_file)
        profile_image.load()

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
        tmp_image_file = io.StringIO()
        profile_image.save(tmp_image_file, "JPEG", quality=90)
        tmp_image_file.seek(0)
        self.profile_image = InMemoryUploadedFile(
            tmp_image_file,
            "ImageField",
            self.profile_image.name,
            "image/jpeg",
            tmp_image_file.len,
            None,
        )
        # Make a Thumbnail Image for the new resized image
        thumb_image = profile_image.copy()
        thumb_image.thumbnail(PROFILE_IMG_THUMB_SIZE, resample=Image.ANTIALIAS)
        tmp_image_file = io.StringIO()
        thumb_image.save(tmp_image_file, "JPEG", quality=90)
        tmp_image_file.seek(0)
        self.profile_image_thumb = InMemoryUploadedFile(
            tmp_image_file,
            "ImageField",
            self.profile_image.name,
            "image/jpeg",
            tmp_image_file.len,
            None,
        )

    def is_full_account(self):
        if self.first_name and self.last_name:
            return True
        else:
            return False

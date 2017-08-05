"""
Account Model
Extends the default django user model
"""
import os
import uuid
import StringIO

from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models
from PIL import Image, ImageOps
from django.core.files.uploadedfile import InMemoryUploadedFile


from utils.constants import US_STATES
from hashtag import Hashtag
from category import Category
from representative import Representative


# Image manipulation constants
PROFILE_IMAGE_SIZE = (171, 171)
PROFILE_IMAGE_THUMB_SIZE = (40, 40)
WHITE_BG = (255,255,255)


class AccountManager(models.Manager):
    def summarize(self, account):
        from civi import Civi
        data = {
            "username": account.user.username,
            "first_name": account.first_name,
            "last_name": account.last_name,
            "about_me": account.about_me,
            "location": account.get_location(),
            "history": [Civi.objects.serialize(c) for c in Civi.objects.filter(author_id=account.id).order_by('-created')],
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
        ellipsis_if_too_long = '' if len(account.about_me) <= about_me_truncate_length else '...'

        data = {
            "id": account.user.id,
            "username": account.user.username,
            "first_name": account.first_name,
            "last_name": account.last_name,
            "about_me": account.about_me[:about_me_truncate_length] + (ellipsis_if_too_long),
            "location": account.get_location(),
            "profile_image": account.profile_image_url,
            "follow_state": True if account in request_account.following.all() else False,
            "request_account": request_account.first_name
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
        extension = filename.split('.')[-1]
        new_filename = str(uuid.uuid4())
        filename = '{}.{}'.format(new_filename, extension)
        return os.path.join(self.sub_path, filename)

profile_upload_path = PathAndRename('')


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=63, blank=False)
    last_name = models.CharField(max_length=63, blank=False)
    about_me = models.CharField(max_length=511, blank=True)

    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=False, default=0)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=False, default=0)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=63, blank=True)
    state = models.CharField(max_length=2, choices=US_STATES, blank=True)
    zip_code = models.CharField(max_length=6, null=True)

    fed_district = models.CharField(max_length=63, default=None, null=True)
    state_district = models.CharField(max_length=63, default=None, null=True)
    representatives = models.ManyToManyField(Representative, related_name='account')

    categories = models.ManyToManyField(Category, related_name='user_categories', symmetrical=False)
    interests = models.ManyToManyField(Hashtag, related_name='interests')
    ai_interests = models.ManyToManyField(Hashtag, related_name='ai_interests')

    followers = models.ManyToManyField('self', related_name='follower', symmetrical=False)
    following = models.ManyToManyField('self', related_name='followings', symmetrical=False)

    beta_access = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    full_account = models.BooleanField(default=False)

    objects = AccountManager()
    profile_image = models.ImageField(upload_to=profile_upload_path, blank=True, null=True)
    profile_image_thumb = models.ImageField(upload_to=profile_upload_path, blank=True, null=True)

    #custom "row-level" functionality (properties) for account models
    def get_location(self):
        """ Constructs a CITY, STATE string for locations in the US """
        if self.city and self.state:
            # Get US State from US States dictionary
            us_state = dict(US_STATES).get(self.state)

            return '{city}, {state}'.format(city=self.city, state=us_state)
        elif self.state:
            # Get US State from US States dictionary
            us_state = dict(US_STATES).get(self.state)

            return '{state}'.format(us_state)
        else:
            return 'NO LOCATION'

    def _get_full_name(self):
        "Returns the person's full name."

        full_name = '{first_name} {last_name}'.format(
            first_name=self.first_name,
            last_name=self.last_name
        )
        return full_name

    full_name = property(_get_full_name)

    def _get_profile_image_url(self):
        """ Return placeholder profile image if user didn't upload one"""

        file_exists = default_storage.exists(
            os.path.join(settings.MEDIA_ROOT, self.profile_image.name)
        )
        if self.profile_image and file_exists:
            return self.profile_image.url
        else:
            #NOTE: This default url will probably be changed later
            return "/static/img/no_image_md.png"

    profile_image_url = property(_get_profile_image_url)

    def __init__(self, *args, **kwargs):
        super(Account, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        """ Image crop/resize and thumbnail creation """

        # New Profile image --
        if self.profile_image:
            self.resize_profile_image()

        super(Account, self).save(*args, **kwargs)

    def resize_profile_image(self):
        profile_image_field = self.profile_image
        image_file = StringIO.StringIO(profile_image_field.read())
        profile_image = Image.open(image_file)
        profile_image.load()

        # Resize image
        profile_image = ImageOps.fit(profile_image, PROFILE_IMAGE_SIZE, Image.ANTIALIAS, centering=(0.5, 0.5))

        # Convert to JPG image format with white background
        if profile_image.mode not in ('L', 'RGB'):
            white_bg_img = Image.new("RGB", PROFILE_IMAGE_SIZE, WHITE_BG)
            white_bg_img.paste(profile_image, mask=profile_image.split()[3])
            profile_image = white_bg_img

        # Create thumb
        tmp_image_file = StringIO.StringIO()
        profile_image.save(tmp_image_file, 'JPEG', quality=90)
        tmp_image_file.seek(0)
        self.profile_image = InMemoryUploadedFile(tmp_image_file, 'ImageField', self.profile_image.name, 'image/jpeg', tmp_image_file.len, None)


        # Make a Thumbnail Image for the new resized image
        thumb_image = profile_image.copy()
        thumb_image.thumbnail(PROFILE_IMAGE_THUMB_SIZE, resample=Image.ANTIALIAS)
        tmp_image_file = StringIO.StringIO()
        thumb_image.save(tmp_image_file, 'JPEG', quality=90)
        tmp_image_file.seek(0)
        self.profile_image_thumb = InMemoryUploadedFile(tmp_image_file, 'ImageField', self.profile_image.name, 'image/jpeg', tmp_image_file.len, None)

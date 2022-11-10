from accounts.models import Profile
from django.contrib.auth import get_user_model
from django.test import TestCase


class BaseTestCase(TestCase):
    """Base test class to set up test cases"""

    def setUp(self) -> None:
        user = get_user_model().objects.create_user(
            username="testuser", email="test@test.com", password="password123"
        )
        self.test_profile, _created = Profile.objects.update_or_create(
            user=user,
            defaults={
                "first_name": "Test",
                "last_name": "User",
                "about_me": "About Me",
            },
        )


class ProfileModelTests(BaseTestCase):
    """A class to test Profile model"""

    def test_profile_creation(self):
        """Whether the fields of created Profile instance is correct"""

        self.assertEqual(self.test_profile.first_name, "Test")
        self.assertEqual(self.test_profile.last_name, "User")
        self.assertEqual(self.test_profile.about_me, "About Me")
        self.assertEqual(self.test_profile.full_name, "Test User")

    def test_profile_has_default_image_url(self):
        """Whether a profile has a default image"""

        self.assertEqual(
            self.test_profile.profile_image_url, "/static/img/no_image_md.png"
        )


class UserModelTest(TestCase):
    """A class to test Profile model"""

    def test_user_create_func_creates_profile(self):
        get_user_model().objects.create_user(
            username="testuser", email="test@test.com", password="password123"
        )
        self.assertEqual(Profile.objects.count(), 1)

    def test_superuser_create_func_creates_profile(self):
        get_user_model().objects.create_superuser(
            username="testuser", email="test@test.com", password="password123"
        )
        self.assertEqual(Profile.objects.count(), 1)

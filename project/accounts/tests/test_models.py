from django.contrib.auth import get_user_model
from django.test import TestCase
from accounts.models import Profile


class BaseTestCase(TestCase):
    """Base test class to set up test cases"""

    def setUp(self) -> None:
        user = get_user_model().objects.create_user(
            username="testuser", email="test@test.com", password="password123"
        )
        self.test_profile, created = Profile.objects.update_or_create(
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


class ProfileManagerTests(BaseTestCase):
    """A class to test ProfileManager"""

    def test_profile_summarize_with_no_history_no_followers_no_following(self):
        """
        Test whether profile summarize is correct
        without history, followers, and followings
        """

        data = {
            "username": self.test_profile.user.username,
            "first_name": self.test_profile.first_name,
            "last_name": self.test_profile.last_name,
            "about_me": self.test_profile.about_me,
            "history": [],
            "profile_image": self.test_profile.profile_image_url,
            "followers": [],
            "following": [],
        }
        self.assertEqual(Profile.objects.summarize(self.test_profile), data)

    def test_profile_chip_summarize(self):
        """Whether profile chip summarize is correct"""

        data = {
            "username": self.test_profile.user.username,
            "first_name": self.test_profile.first_name,
            "last_name": self.test_profile.last_name,
            "profile_image": self.test_profile.profile_image_url,
        }
        self.assertEqual(Profile.objects.chip_summarize(self.test_profile), data)

    def test_profile_card_summarize(self):
        """Whether profile card summarize is correct"""

        data = {
            "id": self.test_profile.user.id,
            "username": self.test_profile.user.username,
            "first_name": self.test_profile.first_name,
            "last_name": self.test_profile.last_name,
            "about_me": self.test_profile.about_me,
            "profile_image": self.test_profile.profile_image_url,
            "follow_state": False,
            "request_profile": self.test_profile.first_name,
        }
        self.assertEqual(
            Profile.objects.card_summarize(
                self.test_profile, Profile.objects.get(user=self.test_profile.user)
            ),
            data,
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

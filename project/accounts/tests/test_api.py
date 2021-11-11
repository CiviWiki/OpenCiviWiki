import json
from PIL import Image
from django.core.files.temp import NamedTemporaryFile
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import Profile
from categories.models import Category
from threads.models import Civi, Thread


class BaseTestCase(TestCase):
    """Base test class to set up test cases"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="newuser", email="test@test.com", password="password123"
        )
        self.user2 = get_user_model().objects.create_user(
            username="newuser2", email="test2@test.com", password="password123"
        )
        self.superuser = get_user_model().objects.create_superuser(
            username="superuser", email="superuser@su.com", password="superpassword123"
        )
        self.user.profile.following.add(self.superuser.profile)
        self.user.profile.followers.add(self.superuser.profile, self.user2.profile)
        self.category = Category.objects.create(name="NewCategory")
        self.user.profile.categories.add(self.category)
        self.thread = Thread.objects.create(
            author=self.user,
            title="Thread",
            summary="summary",
            category=self.category,
            is_draft=False,
        )
        self.draft_thread = Thread.objects.create(
            author=self.user,
            title="Draft Thread",
            summary="draft_summary",
            category=self.category,
        )
        self.civi = Civi.objects.create(
            author=self.user, thread=self.thread, title="Civi", body="body"
        )

    def tearDown(self) -> None:
        self.client.logout()


class ProfileViewSetTests(BaseTestCase):
    """A class to test ProfileViewSet"""

    def test_anonymous_user_cannot_list_profile(self):
        """Whether unauthenticated users cannot list profiles"""

        response = self.client.get(reverse("profile-list"))
        self.assertEqual(response.status_code, 401)

    def test_users_can_list_only_their_profiles(self):
        """Whether authenticated users can only get their own profiles"""

        self.client.login(username="newuser", password="password123")
        response = self.client.get(reverse("profile-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_superusers_can_list_all_profiles(self):
        """Whether superusers can get all profiles"""

        self.client.login(username="superuser", password="superpassword123")
        response = self.client.get(reverse("profile-list"))
        self.assertEqual(response.status_code, 200)
        number_of_profiles = Profile.objects.count()
        self.assertEqual(len(response.data), number_of_profiles)

    def test_users_can_retrive_their_profiles_serialized_by_profileserializer(self):
        """Whether ProfileSerializer is used when users get their profiles"""

        self.client.login(username="newuser", password="password123")
        response = self.client.get(reverse("profile-detail", args=["newuser"]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)
        self.assertIn("about_me", response.data)
        self.assertIn("is_staff", response.data)

    def test_other_users_profiles_retrived_by_serialized_by_profilelistserializer(self):
        """Whether ProfileListSerializer is used when users get their profiles"""

        self.client.login(username="newuser", password="password123")
        response = self.client.get(reverse("profile-detail", args=["newuser2"]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("username", response.data)
        self.assertNotIn("email", response.data)
        self.assertNotIn("about_me", response.data)
        self.assertNotIn("is_staff", response.data)

    def test_only_get_published_threads(self):
        """Whether only published threads can be retrieved"""

        response = self.client.get(reverse("profile-threads", args=["newuser"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertNotEqual(response.data[0]["title"], "Draft Thread")
        self.assertFalse(response.data[0]["is_draft"])

    def test_only_get_draft_threads(self):
        """Whether only draft threads can be retrieved"""

        response = self.client.get(reverse("profile-drafts", args=["newuser"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Draft Thread")
        self.assertTrue(response.data[0]["is_draft"])

    def test_get_civis_created_by_a_user(self):
        """Whether civis of a user can be retrieved"""

        response = self.client.get(reverse("profile-civis", args=["newuser"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Civi")

    def test_get_followers(self):
        """Whether followers of a user can be retrieved"""

        response = self.client.get(reverse("profile-followers", args=["newuser"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), self.user.profile.followers.count())

    def test_get_followings(self):
        """Whether followings of a user can be retrieved"""

        response = self.client.get(reverse("profile-following", args=["newuser"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), self.user.profile.following.count())

    def test_get_categories_followed_by_a_user(self):
        """Whether categories followed by a user can be retrieved"""

        response = self.client.get(reverse("profile-categories", args=["newuser"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), self.user.profile.categories.count())


class GetUserTests(BaseTestCase):
    """A class to test get_user function"""

    def test_existing_user_account_data(self):
        """Whether a user is retrieved"""

        self.client.login(username="newuser", password="password123")
        response = self.client.get(reverse("get_user", args=["newuser"]))
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["username"], self.user.username)

    def test_nonexistent_user_account_data(self):
        """Whether retrieving a nonexistent user raises 404"""

        self.client.login(username="newuser", password="password123")
        response = self.client.get(reverse("get_user", args=["newuser" + "not_exist"]))
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertIn("not found", content["error"])


class GetProfileTests(BaseTestCase):
    """A class to test get_profile function"""

    def test_existing_user_profile_data(self):
        """Whether a user profile is retrieved"""

        self.client.login(username="newuser", password="password123")
        response = self.client.get(reverse("get_profile", args=["newuser"]))
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["username"], self.user.username)

    def test_nonexistent_user_profile_data(self):
        """Whether retrieving a nonexistent user profile raises 404"""

        self.client.login(username="newuser", password="password123")
        response = self.client.get(
            reverse("get_profile", args=["newuser" + "not_exist"])
        )
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertIn("not found", content["error"])


class GetCardTests(BaseTestCase):
    """A class to test get_card function"""

    def test_existing_user_profile_data(self):
        """Whether a user card is retrieved"""

        self.client.login(username="newuser", password="password123")
        response = self.client.get(reverse("get_card", args=["newuser"]))
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["username"], self.user.username)
        self.assertFalse(content["follow_state"])
        response = self.client.get(reverse("get_card", args=["superuser"]))
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["username"], self.superuser.username)
        self.assertTrue(content["follow_state"])

    def test_nonexistent_user_profile_data(self):
        """Whether retrieving a nonexistent user card raises 404"""

        self.client.login(username="newuser", password="password123")
        response = self.client.get(reverse("get_card", args=["newuser" + "not_exist"]))
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertIn("not found", content["error"])


class EditUserTests(BaseTestCase):
    """A class to test edit_user function"""

    def test_first_name_last_name_about_fields_can_be_editable(self):
        """Whether first_name, last_name and about_me fields can be edited"""

        self.client.login(username="newuser", password="password123")
        data = {"first_name": "First", "last_name": "Last", "about_me": "About me"}
        response = self.client.post(reverse("edit_user"), data=data)
        self.user.profile.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.profile.first_name, "First")
        self.assertEqual(self.user.profile.last_name, "Last")
        self.assertEqual(self.user.profile.about_me, "About me")


class UploadProfileImage(BaseTestCase):
    """A class to test upload_profile_image function"""

    def setUp(self) -> None:
        super(UploadProfileImage, self).setUp()
        self.client.login(username="newuser", password="password123")
        self.url = reverse("upload_profile")
        self.image = Image.new("RGB", size=(5, 5), color=(0, 0, 0))
        self.file = NamedTemporaryFile(suffix=".jpg")
        self.image.save(self.file)

    def tearDown(self) -> None:
        for profile in Profile.objects.all():
            profile.profile_image.delete()
            profile.profile_image_thumb.delete()

    def test_upload_profile_image(self):
        """Whether upload_profile_image function works as expected"""

        with open(self.file.name, "rb") as image_file:
            data = {"profile_image": image_file}
            response = self.client.post(self.url, data=data)
            content = json.loads(response.content)
            self.user.profile.refresh_from_db()
            self.assertEqual(
                content.get("profile_image"), self.user.profile.profile_image_url
            )
            self.assertNotEqual(
                self.user.profile.profile_image_url, "/static/img/no_image_md.png"
            )
            self.assertNotEqual(
                self.user.profile.profile_image_thumb_url, "/static/img/no_image_md.png"
            )

    def test_upload_profile_image_with_invalid_extension(self):
        """Whether upload_profile_image raises an error when non-image file is past"""

        image = Image.new("RGB", size=(5, 5), color=(0, 0, 0))
        file = NamedTemporaryFile(suffix=".pdf")
        image.save(file)

        with open(file.name, "rb") as image_file:
            data = {"profile_image": image_file}
            response = self.client.post(self.url, data=data)
            content = json.loads(response.content)
            self.assertEqual(content["error"], "FORM_ERROR")
            self.user.profile.refresh_from_db()
            self.assertEqual(
                self.user.profile.profile_image_url, "/static/img/no_image_md.png"
            )
            self.assertEqual(
                self.user.profile.profile_image_thumb_url, "/static/img/no_image_md.png"
            )


class RequestFollowTests(BaseTestCase):
    """A class to test request_follow function"""

    def test_request_follow(self):
        """Whether request_follow function works as expected"""

        self.client.login(username="newuser", password="password123")
        number_of_followings = self.user.profile.following.count()
        data = {"target": self.user2.username}
        response = self.client.post(reverse("follow_user"), data=data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content.get("result").get("username"), self.user2.username)
        self.assertTrue(content.get("result").get("follow_status"))
        self.assertEqual(self.user.profile.following.count(), number_of_followings + 1)

    def test_user_cannot_follow_itself(self):
        """Whether a user trying to follow itself raises an error"""

        self.client.login(username="newuser", password="password123")
        data = {"target": self.user.username}
        response = self.client.post(reverse("follow_user"), data=data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertIn("You cannot follow yourself", content.get("error"))

    def test_following_nonexistent_user_gives_error(self):
        """Whether following a nonexistent user raises an error"""

        self.client.login(username="newuser", password="password123")
        data = {"target": "nonexistent"}
        response = self.client.post(reverse("follow_user"), data=data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertIn("not found", content.get("error"))


class RequestUnfollowTests(BaseTestCase):
    """A class to test request_unfollow function"""

    def test_request_unfollow(self):
        """Whether request_unfollow function works as expected"""

        self.client.login(username="newuser", password="password123")
        number_of_followings = self.user.profile.following.count()
        data = {"target": self.superuser.username}
        response = self.client.post(reverse("unfollow_user"), data=data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content.get("result"), "Success")
        self.assertEqual(self.user.profile.following.count(), number_of_followings - 1)

    def test_username_for_unfollowing_cannot_be_empty(self):
        """Whether unfollowing an empty username raises an error"""

        self.client.login(username="newuser", password="password123")
        data = {"target": ""}
        response = self.client.post(reverse("unfollow_user"), data=data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content.get("error"), "username cannot be empty")

    def test_unfollowing_nonexistent_user_gives_error(self):
        """Whether unfollowing an nonexistent user raises an error"""

        self.client.login(username="newuser", password="password123")
        data = {"target": "nonexistent"}
        response = self.client.post(reverse("unfollow_user"), data=data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertIn("not found", content.get("error"))

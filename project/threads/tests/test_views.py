import json
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from categories.models import Category
from threads.models import Civi, Thread
import pytest
from pytest_django.asserts import assertTemplateUsed

class BaseTestCase(TestCase):
    """Base test class to set up test cases"""

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="newuser", email="test@test.com", password="password123"
        )
        self.user2 = get_user_model().objects.create_user(
            username="newuser2", email="test2@test.com", password="password123"
        )
        self.superuser = get_user_model().objects.create_superuser(
            username="superuser", email="superuser@su.com", password="superpassword123"
        )
        self.user.profile.first_name = "First"
        self.user.profile.last_name = "Last"
        self.user.profile.about_me = "About Me"
        self.user.profile.save()
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


class ThreadViewSetTests(BaseTestCase):
    """A class to test ThreadViewSet"""

    def setUp(self) -> None:
        super(ThreadViewSetTests, self).setUp()
        self.client = APIClient()

    def test_anonymous_user_can_list_threads(self):
        """Whether unauthenticated users cannot list profiles"""

        response = self.client.get(reverse("thread-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_authenticated_users_can_list_threads(self):
        """Whether authenticated users can only get their own profiles"""

        self.client.login(username="newuser", password="password123")
        response = self.client.get(reverse("thread-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_retrieving_civis(self):
        """Whether civi:id is retrieved"""

        response = self.client.get(reverse("thread-civis", args=["1"]))
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content[0].get("title"), "Civi")

    def test_list_all_threads_via_all(self):
        """Whether all threads are listed"""

        response = self.client.get(reverse("thread-all"))
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 2)

    def test_users_can_only_get_their_draft_threads(self):
        """Whether users can only get their draft threads"""

        self.client.login(username=self.user.username, password="password123")
        response = self.client.get(reverse("thread-drafts"))
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0].get("title"), "Draft Thread")

    def test_users_cannot_get_draft_threads_of_another_users(self):
        """Whether users cannot get other users' draft threads"""

        self.client.login(username=self.user2.username, password="password123")
        response = self.client.get(reverse("thread-drafts"))
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 0)


class BaseViewTests(BaseTestCase):
    """A class to test base_view function"""

    def setUp(self) -> None:
        super(BaseViewTests, self).setUp()
        self.client.login(username=self.user.username, password="password123")
        self.url = reverse("base")
        self.response = self.client.get(self.url)

    def test_anonymous_users_are_redirected_to_landing_page(self):
        """Whether unauthenticated users are redirected to the landing page"""

        self.client.logout()
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 200)
        # self.assertTemplateUsed(self.response, "base.html")
        self.assertTemplateUsed(self.response, "landing.html")
        self.assertTemplateUsed(self.response, "static_nav.html")
        self.assertTemplateUsed(self.response, "static_footer.html")
        self.assertContains(self.response, "Why CiviWiki?")
        self.assertNotContains(self.response, "Wrong Content!")

    def test_authenticated_users_are_redirected_to_feed_page(self):
        """Whether authenticated users are redirected to the feed page"""

        self.assertEqual(self.response.status_code, 200)
        # self.assertTemplateUsed(self.response, "base.html")
        self.assertTemplateUsed(self.response, "feed.html")
        self.assertTemplateUsed(self.response, "global_nav.html")
        self.assertTemplateUsed(self.response, "static_footer.html")
        self.assertContains(self.response, "Trending Issues")
        self.assertNotContains(self.response, "Wrong Content!")


class IssueThreadTests(BaseTestCase):
    """A class to test issue_thread function"""

    def setUp(self) -> None:
        super(IssueThreadTests, self).setUp()
        self.client.login(username=self.user.username, password="password123")

    def test_nonexistent_threads_redirect_to_404_page(self):
        """Whether getting nonexistent threads redirects to 404 page"""

        url = reverse("thread-detail", args=["12345"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_existing_threads(self):
        """Whether existing threads are retrieved as expected"""

        url = reverse("thread-detail", args=["1"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

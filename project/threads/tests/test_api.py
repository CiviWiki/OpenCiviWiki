import json
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
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


class NewThreadTests(BaseTestCase):
    """A class to test new_thread function"""

    def test_creation_of_a_new_thread(self):
        """Whether a new thread is created as expected"""

        number_of_threads = self.user.thread_set.count()
        thread_data = {
            "title": "New Thread",
            "summary": "Summary",
            "category_id": self.category.id,
        }
        self.client.login(username="newuser", password="password123")
        response = self.client.post(reverse("new thread"), data=thread_data)
        content = json.loads(response.content)
        self.assertEqual(self.user.thread_set.count(), number_of_threads + 1)
        self.assertEqual(content.get("data"), "success")
        self.assertEqual(content.get("thread_id"), self.user.thread_set.last().id)


class GetThreadTests(BaseTestCase):
    """A class to test get_thread function"""

    def test_get_thread(self):
        """Whether a thread is retrieved as expected"""

        self.client.login(username="newuser", password="password123")
        response = self.client.get(reverse("get thread", args=[self.thread.id]))
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["title"], "Thread")
        self.assertEqual(content["author"]["username"], "newuser")
        self.assertEqual(content["category"]["name"], "NewCategory")


class EditThreadTests(BaseTestCase):
    """A class to test edit_thread function"""

    def test_edit_thread(self):
        """Whether a thread is edited as expected"""

        self.client.login(username="newuser", password="password123")
        data = {
            "thread_id": self.thread.id,
            "title": "Edited Title",
            "summary": "Edited summary",
        }
        response = self.client.post(reverse("edit thread"), data=data)
        content = json.loads(response.content)
        self.thread.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.thread.title, "Edited Title")
        self.assertEqual(self.thread.summary, "Edited summary")
        self.assertEqual(int(content["data"]["thread_id"]), self.thread.id)

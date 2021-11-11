import os
import json
from PIL import Image
from django.conf import settings
from django.core.files.temp import NamedTemporaryFile
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from categories.models import Category
from threads.models import Civi, CiviImage, Thread


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


class CreateCiviTests(BaseTestCase):
    """A class to test create_civi function"""

    def test_create_new_civi(self):
        """Whether a new civi is created as expected"""

        new_civi_data = {
            "thread_id": self.thread.pk,
            "title": "New Civi",
            "body": "New Body",
            "c_type": self.category.name,
        }
        self.client.login(username="newuser", password="password123")
        response = self.client.post(reverse("new civi"), data=new_civi_data)
        content = json.loads(response.content)
        self.assertEqual(content["data"]["thread_id"], self.thread.id)
        self.assertEqual(content["data"]["title"], "New Civi")
        self.assertEqual(content["data"]["body"], "New Body")
        self.assertEqual(content["data"]["author"]["username"], self.user.username)


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

    def test_edit_nonexistent_thread(self):
        """Whether editing a nonexistent thread gives 400 HTTP Status Code"""

        self.client.login(username="newuser", password="password123")
        data = {
            "thread_id": 12345,
            "title": "Edited Title",
            "summary": "Edited summary",
        }
        response = self.client.post(reverse("edit thread"), data=data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertIn("does not exist", content["error"])

    def test_edit_thread_with_missing_id_field(self):
        """Whether editing a thread with_missing id field gives 400 HTTP Status Code"""

        self.client.login(username="newuser", password="password123")
        data = {
            "title": "Edited Title",
            "summary": "Edited summary",
        }
        response = self.client.post(reverse("edit thread"), data=data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content["error"], "Invalid Thread Reference")


class EditCiviTests(BaseTestCase):
    """A class to test edit_civi function"""

    def test_edit_civi(self):
        """Whether a civi is edited as expected"""

        self.client.login(username="newuser", password="password123")
        data = {
            "civi_id": self.civi.id,
            "title": "Edited Civi",
            "body": "Edited body",
        }
        response = self.client.post(reverse("edit civi"), data=data)
        content = json.loads(response.content)
        self.civi.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.civi.title, "Edited Civi")
        self.assertEqual(self.civi.body, "Edited body")
        self.assertEqual(content.get("thread_id"), 1)
        self.assertEqual(content.get("title"), "Edited Civi")

    def test_edit_nonexistent_civi(self):
        """Whether editing a nonexistent civi gives 400 HTTP Status Code"""

        self.client.login(username="newuser", password="password123")
        data = {
            "civi_id": 12345,
            "title": "Edited Civi",
            "body": "Edited body",
        }
        response = self.client.post(reverse("edit civi"), data=data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertIn("does not exist", content["error"])


class DeleteCiviTests(BaseTestCase):
    """A class to test delete_civi function"""

    def test_delete_civi(self):
        """Whether a civi is deleted as expected"""

        number_of_civis = Civi.objects.count()
        self.client.login(username="newuser", password="password123")
        data = {"civi_id": self.civi.id}
        response = self.client.post(reverse("delete civi"), data=data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content.get("result"), "Success")
        self.assertEqual(Civi.objects.count(), number_of_civis - 1)

    def test_only_civi_authors_have_right_to_delete(self):
        """Whether only owner of a civi can delete the civi"""

        self.client.login(username="newuser2", password="password123")
        data = {"civi_id": self.civi.id}
        response = self.client.post(reverse("delete civi"), data=data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content.get("error"), "No Edit Rights")


class UploadThreadImageTests(BaseTestCase):
    """A class to test upload_thread_image function"""

    def setUp(self) -> None:
        super(UploadThreadImageTests, self).setUp()
        self.client.login(username="newuser", password="password123")
        self.url = reverse("upload image")
        self.image = Image.new("RGB", size=(5, 5), color=(0, 0, 0))
        self.file = NamedTemporaryFile(suffix=".jpg")
        self.image.save(self.file)

    def tearDown(self) -> None:
        """Delete test thread images from the file system"""

        for thread in Thread.objects.all():
            thread.image.delete()

    def test_upload_thread_image(self):
        """Whether a thread image is uploaded as expected"""

        with open(self.file.name, "rb") as image_file:
            data = {"thread_id": self.thread.id, "attachment_image": image_file}
            response = self.client.post(self.url, data=data)
            content = json.loads(response.content)
            self.thread.refresh_from_db()
            self.assertEqual(content.get("image"), self.thread.image_url)
            self.assertNotEqual(self.thread.image_url, "/static/img/no_image_md.png")


class UploadCiviImageTests(BaseTestCase):
    """A class to test upload_civi_image function"""

    def setUp(self) -> None:
        super(UploadCiviImageTests, self).setUp()
        self.client.login(username="newuser", password="password123")
        self.url = reverse("upload images")
        self.image = Image.new("RGB", size=(5, 5), color=(0, 0, 0))
        self.file = NamedTemporaryFile(suffix=".jpg")
        self.image.save(self.file)

    def tearDown(self) -> None:
        """Delete test civi images from the file system"""

        for civi_image in CiviImage.objects.all():
            image_path = os.path.join(settings.BASE_DIR, civi_image.image_url[1:])
            if os.path.isfile(image_path):
                os.remove(image_path)

    def test_upload_civi_image(self):
        """Whether a civi image is uploaded as expected"""

        with open(self.file.name, "rb") as image_file:
            data = {"civi_id": self.civi.id, "attachment_image": image_file}
            response = self.client.post(self.url, data=data)
            content = json.loads(response.content)
            self.thread.refresh_from_db()
            self.assertEqual(
                content.get("attachments")[0].get("image_url"),
                self.civi.images.first().image_url,
            )
            self.assertNotEqual(
                self.civi.images.first().image_url, "/static/img/no_image_md.png"
            )

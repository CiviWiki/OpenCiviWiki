from django.contrib.auth import get_user_model
from django.test import TestCase
from accounts.forms import UserRegistrationForm


class UserRegistrationFormTest(TestCase):
    """A class to test user registration form"""

    def setUp(self) -> None:
        self.data = {
            "username": "testuser",
            "email": "test@test.com",
            "password": "password123",
        }

    def test_user_creation_form_with_success(self):
        """Whether form works as expected for the valid inputs"""

        form = UserRegistrationForm(self.data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.errors, {})
        form.save()
        self.assertTrue(get_user_model().objects.count(), 1)

    def test_form_is_unsuccessful_for_short_password(self):
        """Whether a user does not have a short password"""

        self.data["password"] = "123"
        form = UserRegistrationForm(self.data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.errors, {})
        self.assertTrue(form.has_error("password"))
        self.assertEqual(get_user_model().objects.count(), 0)

    def test_form_is_unsuccessful_for_only_digit_password(self):
        """Whether a user does not have an only-digit password"""

        self.data["password"] = "12345678"
        form = UserRegistrationForm(self.data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.errors, {})
        self.assertTrue(form.has_error("password"))
        self.assertEqual(get_user_model().objects.count(), 0)

    def test_form_is_unsuccessful_for_invalid_username(self):
        """Whether a user does not have an invalid username"""

        self.data["username"] = "......."
        form = UserRegistrationForm(self.data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.errors, {})
        self.assertTrue(form.has_error("username"))
        self.assertEqual(get_user_model().objects.count(), 0)

    def test_form_is_unsuccessful_for_existing_username_and_email(self):
        """Whether a user does not have an existing username and email"""

        form = UserRegistrationForm(self.data)
        form.save()
        form = UserRegistrationForm(self.data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.errors, {})
        self.assertTrue(form.has_error("username"))
        self.assertTrue(form.has_error("email"))
        self.assertEqual(get_user_model().objects.count(), 1)

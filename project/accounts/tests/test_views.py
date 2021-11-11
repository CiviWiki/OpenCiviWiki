from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views
from accounts.models import Profile
from accounts.views import RegisterView


class BaseTestCase(TestCase):
    """Base test class to set up test cases"""

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="newuser", email="test@test.com", password="password123"
        )


class LoginViewTests(BaseTestCase):
    """A class to test login view"""

    def setUp(self) -> None:
        super(LoginViewTests, self).setUp()
        url = reverse("accounts_login")
        self.response = self.client.get(url)

    def test_login_template(self):
        """Whether login view uses the correct template"""

        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "accounts/register/login.html")
        self.assertContains(self.response, "Log In")
        self.assertNotContains(self.response, "Wrong Content!")

    def test_login_url_matches_with_login_view(self):
        """Whether login URL matches with the correct view"""

        view = resolve("/login/")
        self.assertEqual(view.func.__name__, auth_views.LoginView.__name__)

    def test_the_user_with_the_correct_credentials_login(self):
        """Whether a user with the correct credentials can login"""

        self.assertTrue(self.client.login(username="newuser", password="password123"))

    def test_login_view_redirects_on_success(self):
        """Whether login view redirects to the base view after the successive try"""

        response = self.client.post(
            reverse("accounts_login"),
            {"username": "newuser", "password": "password123"},
        )
        self.assertRedirects(
            response,
            expected_url=reverse("base"),
            status_code=302,
            target_status_code=200,
        )


class RegisterViewTests(TestCase):
    """A class to test register view"""

    def setUp(self):
        self.url = reverse("accounts_register")

    def test_register_template(self):
        """Whether register view uses the correct template"""

        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "accounts/register/register.html")
        self.assertTemplateNotUsed(self.response, "accounts/register.html")
        self.assertContains(self.response, "Register")
        self.assertNotContains(self.response, "Wrong Content!")

    def test_register_url_matches_with_register_view(self):
        """Whether register URL matches with the correct view"""

        view = resolve("/register/")
        self.assertEqual(view.func.__name__, RegisterView.__name__)

    def test_register_view_creates_a_user_successfully(self):
        """Whether register view creates a new user with success"""

        user_count = get_user_model().objects.count()
        self.client.post(
            reverse("accounts_register"),
            {
                "username": "newuser",
                "email": "newuser@email.com",
                "password": "password123",
            },
        )
        self.assertEqual(get_user_model().objects.count(), user_count + 1)

    def test_register_view_redirects_on_success(self):
        """Whether register view redirects to the base view after the successive try"""

        response = self.client.post(
            reverse("accounts_register"),
            {
                "username": "newuser",
                "email": "newuser@email.com",
                "password": "password123",
            },
        )
        self.assertRedirects(
            response,
            expected_url=reverse("base"),
            status_code=302,
            target_status_code=200,
        )


class SettingsViewTests(BaseTestCase):
    """A class to test settings view"""

    def setUp(self) -> None:
        super(SettingsViewTests, self).setUp()
        self.user.profile.first_name = "Gorkem"
        self.user.profile.last_name = "Arslan"
        self.user.profile.save()
        self.client.login(username=self.user.username, password="password123")
        self.url = reverse("accounts_settings")
        self.response = self.client.get(self.url)

    def test_template_name(self):
        """Whether the correct template is used"""

        self.assertTemplateUsed(self.response, "accounts/update_settings.html")

    def test_contains_existing_data(self):
        """Whether the existing data is available"""

        self.assertContains(self.response, "Gorkem")
        self.assertContains(self.response, "Arslan")

    def test_anonymous_users_are_redirected_to_login_page(self):
        """Whether anonymous users are redirected to the login page"""

        self.client.logout()
        self.response = self.client.get(self.url)
        expected_url = (
            reverse("accounts_login") + "?next=" + reverse("accounts_settings")
        )
        self.assertRedirects(
            response=self.response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200,
            msg_prefix="",
            fetch_redirect_response=True,
        )


class ProfileActivationViewTests(TestCase):
    """A class to test profile activation view"""

    def setUp(self) -> None:
        self.response = self.client.post(
            reverse("accounts_register"),
            {
                "username": "newuser",
                "email": "newuser@email.com",
                "password": "password123",
            },
        )
        self.user = get_user_model().objects.get(username="newuser")
        self.profile = Profile.objects.get(user=self.user)
        self.activation_link = self.response.context[0]["link"]

    def test_activation_link(self):
        """Whether the activation link works as expected"""

        self.assertFalse(self.profile.is_verified)
        response = self.client.get(self.activation_link)
        self.profile.refresh_from_db()
        self.assertTrue(self.profile.is_verified)
        self.assertTemplateUsed(response, "general_message.html")
        self.assertContains(response, "Email Verification Successful")

    def test_activation_link_with_a_verified_user(self):
        """Whether a verified user is welcomed by already verified page"""

        self.client.get(self.activation_link)
        response = self.client.get(self.activation_link)
        self.assertTemplateUsed(response, "general_message.html")
        self.assertContains(response, "Email Already Verified")

    def test_invalid_action_link(self):
        """Whether a verified user is welcomed by verification error page"""

        invalid_link = self.activation_link[:-10] + "12345/"
        response = self.client.get(invalid_link)
        self.assertFalse(self.profile.is_verified)
        self.assertTemplateUsed(response, "general_message.html")
        self.assertContains(response, "Email Verification Error")


class UserProfileView(BaseTestCase):
    """A class to test user profile view"""

    def setUp(self) -> None:
        super(UserProfileView, self).setUp()
        self.user.profile.first_name = "First"
        self.user.profile.last_name = "Last"
        self.user.profile.about_me = "About"
        self.user.profile.save()

    def test_get_user_profile(self):
        """Whether user_profile function works as expected"""

        self.client.login(username="newuser", password="password123")
        response = self.client.get(reverse("profile", args=["newuser"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.user.email)
        self.assertTemplateUsed(response, "account.html")

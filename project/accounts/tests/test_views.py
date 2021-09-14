from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views
from accounts.models import Profile
from accounts.views import RegisterView


class BaseTestCase(TestCase):
    """Base test class to set up test cases"""

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(username="newuser",
                                                         email="test@test.com",
                                                         password="password123")
        self.profile = Profile.objects.create(user=self.user)


class LoginViewTests(BaseTestCase):
    """A class to test login view"""

    def setUp(self) -> None:
        super(LoginViewTests, self).setUp()
        url = reverse('accounts_login')
        self.response = self.client.get(url)

    def test_login_template(self):
        """Whether login view uses the correct template"""

        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'accounts/register/login.html')
        self.assertTemplateNotUsed(self.response, 'accounts/login.html')
        self.assertContains(self.response, 'Log In')
        self.assertNotContains(self.response, 'Wrong Content!')

    def test_login_url_matches_with_login_view(self):
        """Whether login URL matches with the correct view"""

        view = resolve('/login/')
        self.assertEqual(view.func.__name__, auth_views.LoginView.__name__)

    def test_the_user_with_the_correct_credentials_login(self):
        """Whether a user with the correct credentials can login"""

        self.assertTrue(self.client.login(username="newuser", password="password123"))

    def test_login_view_redirects_on_success(self):
        """Whether login view redirects to the base view after the successive try"""

        response = self.client.post(reverse('accounts_login'),
                                    {'username': "newuser",
                                     'password': "password123"})
        self.assertRedirects(response, expected_url=reverse('base'), status_code=302, target_status_code=200)


class RegisterViewTests(TestCase):
    """A class to test register view"""

    def setUp(self):
        self.url = reverse('accounts_register')

    def test_register_template(self):
        """Whether register view uses the correct template"""

        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'accounts/register/register.html')
        self.assertTemplateNotUsed(self.response, 'accounts/register.html')
        self.assertContains(self.response, 'Register')
        self.assertNotContains(self.response, 'Wrong Content!')

    def test_register_url_matches_with_register_view(self):
        """Whether register URL matches with the correct view"""

        view = resolve('/register/')
        self.assertEqual(view.func.__name__, RegisterView.__name__)

    def test_register_view_creates_a_user_successfully(self):
        """Whether register view creates a new user with success"""

        user_count = get_user_model().objects.count()
        self.client.post(reverse('accounts_register'),
                         {'username': "newuser",
                          "email": "newuser@email.com",
                          'password': "password123"})
        self.assertEqual(get_user_model().objects.count(), user_count + 1)

    def test_register_view_redirects_on_success(self):
        """Whether register view redirects to the base view after the successive try"""

        response = self.client.post(reverse('accounts_register'),
                                    {'username': "newuser",
                                     "email": "newuser@email.com",
                                     'password': "password123"})
        self.assertRedirects(response, expected_url=reverse('base'), status_code=302, target_status_code=200)

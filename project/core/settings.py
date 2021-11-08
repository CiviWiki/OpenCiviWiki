"""
Django settings for civiwiki project.
Darius Calliet May 12, 2016

Production settings file to select proper environment variables.
"""
import os

# False if not in os.environ
DEBUG = os.getenv("DEBUG", False)

# defaults to second value if not found in os.environ
DJANGO_HOST = os.getenv("DJANGO_HOST", "LOCALHOST")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "TEST_KEY_FOR_DEVELOPMENT")
ALLOWED_HOSTS = [".herokuapp.com", ".civiwiki.org", "127.0.0.1", "localhost", "0.0.0.0"]

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "storages",
    "core",
    "rest_framework",
    "accounts.apps.AccountsConfig",
    "threads",
    "notifications",
    "corsheaders",
    "taggit",
    "categories",
    "notification",
)

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CSRF_USE_SESSIONS = (
    True  # Store the CSRF token in the users session instead of in a cookie
)

CORS_ORIGIN_ALLOW_ALL = True
ROOT_URLCONF = "core.urls"

# SSL Setup
if DJANGO_HOST != "LOCALHOST":
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Internationalization & Localization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "threads/templates/threads"),
            os.path.join(BASE_DIR, "accounts/templates/accounts"),
        ],  # TODO: Add non-webapp template directory
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Apex Contact for Production Errors
ADMINS = [("Development Team", "dev@civiwiki.org")]

STATIC_URL = "/static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "core/templates/static"),)
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# TODO: re-organize and simplify staticfiles settings
if "CIVIWIKI_LOCAL_NAME" not in os.environ:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Use DATABASE_URL in production
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is not None:
    DATABASES = {"default": DATABASE_URL}
else:
    # Default to sqlite for simplicity in development
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR + "/" + "db.sqlite3",
        }
    }

# Email Backend Setup
if "EMAIL_HOST" not in os.environ:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    EMAIL_HOST_USER = "test@civiwiki.org"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = os.getenv("EMAIL_PORT")
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
    EMAIL_USE_SSL = True
    DEFAULT_FROM_EMAIL = EMAIL_HOST

# Notification API Settings
NOTIFICATIONS_SOFT_DELETE = True
NOTIFICATIONS_USE_JSONFIELD = True

# Django REST API Settings
DEFAULT_RENDERER_CLASSES = ("rest_framework.renderers.JSONRenderer",)

if DEBUG:
    # Browsable HTML - Enabled only in Debug mode (dev)
    DEFAULT_RENDERER_CLASSES = DEFAULT_RENDERER_CLASSES + (
        "rest_framework.renderers.BrowsableAPIRenderer",
    )

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_RENDERER_CLASSES": DEFAULT_RENDERER_CLASSES,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
}

# CORS Settings
CORS_ORIGIN_ALLOW_ALL = True

# Custom User model
AUTH_USER_MODEL = "accounts.User"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Login Logout URLS
LOGIN_URL = "login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 4,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

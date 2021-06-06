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
    "core",  # TODO: consider removing this, if we can move the decorators, etc. to an actual app
    "api",
    "rest_framework",
    "accounts",
    "threads",
    "frontend_views",
    "notifications",
    "corsheaders",
    "taggit",
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
LOGIN_URL = "/login"

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
            os.path.join(BASE_DIR, "webapp/templates")
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

# AWS S3 Setup
if "AWS_STORAGE_BUCKET_NAME" not in os.environ:
    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
else:
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_ACCESS_KEY_ID = os.getenv("AWS_S3_ACCESS_KEY_ID")
    AWS_S3_SECRET_ACCESS_KEY = os.getenv("AWS_S3_SECRET_ACCESS_KEY")
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto.S3BotoStorage"
    AWS_S3_SECURE_URLS = False
    AWS_QUERYSTRING_AUTH = False

STATIC_URL = "/static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "webapp/static"),)
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

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

DEFAULT_AUTHENTICATION_CLASSES = ("rest_framework.authentication.BasicAuthentication",)

if DEBUG:
    # Browsable HTML - Enabled only in Debug mode (dev)
    DEFAULT_RENDERER_CLASSES = DEFAULT_RENDERER_CLASSES + (
        "rest_framework.renderers.BrowsableAPIRenderer",
    )

    DEFAULT_AUTHENTICATION_CLASSES = (
        "api.authentication.CsrfExemptSessionAuthentication",
    ) + DEFAULT_AUTHENTICATION_CLASSES

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_RENDERER_CLASSES": DEFAULT_RENDERER_CLASSES,
    "DEFAULT_AUTHENTICATION_CLASSES": DEFAULT_AUTHENTICATION_CLASSES,
}

# CORS Settings
CORS_ORIGIN_ALLOW_ALL = True


# Custom User model
AUTH_USER_MODEL = 'accounts.User'


LOGIN_REDIRECT_URL = '/beta'

APPEND_SLASH = False


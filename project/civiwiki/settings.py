"""
Django settings for civiwiki project.
Darius Calliet May 12, 2016

Production settings file to select proper environment variables.
"""
import os

# False if not in os.environ
DEBUG = os.getenv("DEBUG",False)

# defaults to second value if not found in os.environ
DJANGO_HOST = os.getenv("DJANGO_HOST","LOCALHOST")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY","TEST_KEY_FOR_DEVELOPMENT")
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
    "channels",
    "civiwiki",
    "api",
    "rest_framework",
    "authentication",
    "frontend_views",
    "notifications",
    "corsheaders",
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
ROOT_URLCONF = "civiwiki.urls"
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

WSGI_APPLICATION = "civiwiki.wsgi.application"

# Global user privilege settings
CLOSED_BETA = os.getenv("CLOSED_BETA", False)

# Apex Contact for Production Errors
ADMINS = [("Development Team", "dev@civiwiki.org")]

# API keys
# returns None if not found in os.environ
SUNLIGHT_API_KEY = os.getenv("SUNLIGHT_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_MAP_API_KEY")

# Channels Setup
REDIS_URL = os.getenv("REDIS_URL", default="redis://localhost:6379")
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL],
        },
        "ROUTING": "civiwiki.routing.channel_routing",
    },
}

# Celery Task Runner Setup
CELERY_BROKER_URL = REDIS_URL + "/0"
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIME_ZONE = TIME_ZONE

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

# Database
if "CIVIWIKI_LOCAL_NAME" not in os.environ:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

    DATABASES = {"default": os.getenv("DATABASE_URL")}
else:
    DATABASES = {
        "default": {
            "HOST": os.getenv("CIVIWIKI_LOCAL_DB_HOST", "localhost"),
            "PORT": "5432",
            "NAME": os.getenv("CIVIWIKI_LOCAL_NAME"),
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "USER": os.getenv("CIVIWIKI_LOCAL_USERNAME"),
            "PASSWORD": os.getenv("CIVIWIKI_LOCAL_PASSWORD"),
        },
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
PROPUBLICA_API_KEY = os.getenv("PROPUBLICA_API_KEY","TEST")

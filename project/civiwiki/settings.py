"""
Django settings for civiwiki project.
Darius Calliet May 12, 2016

Production settings file to select proper environment variables.
"""
import os

from django.core.exceptions import ImproperlyConfigured
import dj_database_url


def get_env_variable(environment_variable, optional=False):
    """Get the environment variable or return exception"""
    try:
        return os.environ[environment_variable]
    except KeyError:
        if optional:
            return ''
        else:
            error = "Environment variable '{ev}' not found.".format(ev=environment_variable)
            raise ImproperlyConfigured(error)


# Devlopment Environment Control
DEBUG = 'DEBUG' in os.environ

if 'DJANGO_HOST' in os.environ:
    DJANGO_HOST = get_env_variable("DJANGO_HOST")
else:
    DJANGO_HOST = 'LOCALHOST'


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = get_env_variable("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = [".herokuapp.com", ".civiwiki.org", "127.0.0.1", "localhost"]


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'channels',
    'civiwiki',
    'api',
    'authentication',
    'frontend_views',
    'notifications',
    'legislation',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)


CSRF_USE_SESSIONS = True # Store the CSRF token in the users session instead of in a cookie

CORS_ORIGIN_ALLOW_ALL = True
ROOT_URLCONF = 'civiwiki.urls'
LOGIN_URL = '/login'


# SSL Setup
if DJANGO_HOST is not 'LOCALHOST':
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


# Internationalization & Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "webapp/templates")], #TODO: Add non-webapp template directory
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'civiwiki.wsgi.application'


# Apex Contact for Production Errors
ADMINS = [('Development Team', 'dev@civiwiki.org')]


# API keys
SUNLIGHT_API_KEY = get_env_variable("SUNLIGHT_API_KEY")
GOOGLE_API_KEY = get_env_variable("GOOGLE_MAP_API_KEY")

# Channels Setup
if 'REDIS_URL' in os.environ:
    REDIS_URL = get_env_variable("REDIS_URL")
else:
    REDIS_URL = 'redis://localhost:6379'
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
CELERY_BROKER_URL = REDIS_URL + '/0'
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIME_ZONE = TIME_ZONE


# AWS S3 Setup
if 'AWS_STORAGE_BUCKET_NAME' not in os.environ:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
else:
    AWS_STORAGE_BUCKET_NAME = get_env_variable("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_ACCESS_KEY_ID = get_env_variable("AWS_S3_ACCESS_KEY_ID")
    AWS_S3_SECRET_ACCESS_KEY = get_env_variable("AWS_S3_SECRET_ACCESS_KEY")
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    AWS_S3_SECURE_URLS = False
    AWS_QUERYSTRING_AUTH = False

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'webapp/static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Database
if 'CIVIWIKI_LOCAL_NAME' not in os.environ:
    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

    DATABASES = {
        'default': dj_database_url.parse(get_env_variable("DATABASE_URL"))
    }
else:
    DATABASES = {
        'default': {
            'HOST': 'localhost',
            'PORT': '5432',
            'NAME': get_env_variable("CIVIWIKI_LOCAL_NAME"),
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'USER': get_env_variable("CIVIWIKI_LOCAL_USERNAME"),
            'PASSWORD': get_env_variable("CIVIWIKI_LOCAL_PASSWORD"),
        },
    }


# Email Backend Setup
if 'EMAIL_HOST' not in os.environ:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    EMAIL_HOST_USER = "test@civiwiki.org"
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = get_env_variable("EMAIL_HOST")
    EMAIL_PORT = get_env_variable("EMAIL_PORT")
    EMAIL_HOST_USER = get_env_variable("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = get_env_variable("EMAIL_HOST_PASSWORD")
    EMAIL_USE_SSL = True
    DEFAULT_FROM_EMAIL = EMAIL_HOST


# Notification API Settings
NOTIFICATIONS_SOFT_DELETE = True
NOTIFICATIONS_USE_JSONFIELD = True

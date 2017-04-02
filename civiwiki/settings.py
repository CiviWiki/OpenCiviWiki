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
            error = "environment variable '{ev}' not found.".format(ev=environment_variable)
            raise ImproperlyConfigured(error)

if 'DEBUG' not in os.environ:
    DEBUG = False
else:
    DEBUG = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = get_env_variable("DJANGO_SECRET_KEY")
SUNLIGHT_API_KEY = get_env_variable("SUNLIGHT_API_KEY")
GOOGLE_API_KEY = "AIzaSyAKMT4cagDtpKz61vy0ByPxGDo2nvvXn4M" #get_env_variable("GOOGLE_MAP_API_KEY")
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
    'api',
    'authentication',
    'frontend_views',
    'notifications',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware', TODO: fix eventually
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

CORS_ORIGIN_ALLOW_ALL = True
ROOT_URLCONF = 'civiwiki.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "webapp/templates")],
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

# Channels Setup
if 'CIVIWIKI_REDIS_URL' not in os.environ:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "asgi_redis.RedisChannelLayer",
            "CONFIG": {
                "hosts": [("localhost", 6379)],
            },
            "ROUTING": "civiwiki.routing.channel_routing",
        },
    }
else:
    REDIS_URL = get_env_variable("CIVIWIKI_REDIS_URL")
    REDIS_PORT = get_env_variable("CIVIWIKI_REDIS_PORT")
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "asgi_redis.RedisChannelLayer",
            "CONFIG": {
                "hosts": [(REDIS_URL, REDIS_PORT)],
            },
            "ROUTING": "civiwiki.routing.channel_routing",
        },
    }

# AWS S3 Setup
AWS_STORAGE_BUCKET_NAME = get_env_variable("AWS_STORAGE_BUCKET_NAME", '')
if AWS_STORAGE_BUCKET_NAME:
    AWS_S3_ACCESS_KEY_ID = get_env_variable("AWS_S3_ACCESS_KEY_ID")
    AWS_S3_SECRET_ACCESS_KEY = get_env_variable("AWS_S3_SECRET_ACCESS_KEY")
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    AWS_S3_SECURE_URLS = False
    AWS_QUERYSTRING_AUTH = False
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")

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


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOGIN_URL = '/login'


# Notification API Settings
NOTIFICATIONS_SOFT_DELETE=True
NOTIFICATIONS_USE_JSONFIELD=True


# Valid US State Choices
US_STATES = (('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'),
            ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'),
            ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'),
            ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'),
            ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'),
            ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'),
            ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'),
            ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'),
            ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'),
            ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'),
            ('WY', 'Wyoming'))

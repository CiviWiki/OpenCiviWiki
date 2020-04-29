
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
# django environ imported
import environ

env = environ.Env()

# reading .env file
environ.Env.read_env()

# Channels Setup
if env('REDIS_URL'):
    REDIS_URL = env.str("REDIS_URL")
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

# Internationalization & Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Celery Task Runner Setup
CELERY_BROKER_URL = REDIS_URL + '/0'
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIME_ZONE = TIME_ZONE


# Global user privilege settings
CLOSED_BETA = False
if env('CLOSED_BETA'):
    CLOSED_BETA = env.str("CLOSED_BETA")



#sentry-sdk

SENTRY_ADDRESS = env('SENTRY_ADDRESS', optional=True)
if SENTRY_ADDRESS:
    sentry_sdk.init(
        dsn=SENTRY_ADDRESS,
        integrations=[DjangoIntegration()]
    )

#django-rest-framework

# Devlopment Environment Control
DEBUG = env('DEBUG')    # False if not in os.environ

# Django REST API Settings
DEFAULT_RENDERER_CLASSES = (
    'rest_framework.renderers.JSONRenderer',
)

DEFAULT_AUTHENTICATION_CLASSES = ('rest_framework.authentication.BasicAuthentication',)

if DEBUG:
    # Browsable HTML - Enabled only in Debug mode (dev)
    DEFAULT_RENDERER_CLASSES = DEFAULT_RENDERER_CLASSES + (
        'rest_framework.renderers.BrowsableAPIRenderer',
    )

    DEFAULT_AUTHENTICATION_CLASSES = (
        'api.authentication.CsrfExemptSessionAuthentication',
    ) + DEFAULT_AUTHENTICATION_CLASSES

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': DEFAULT_RENDERER_CLASSES,
    'DEFAULT_AUTHENTICATION_CLASSES': DEFAULT_AUTHENTICATION_CLASSES
}


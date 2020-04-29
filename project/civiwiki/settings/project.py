import environ

env = environ.Env()

# reading .env file
environ.Env.read_env()

# CORS Settings
CORS_ORIGIN_ALLOW_ALL = True

# API keys
SUNLIGHT_API_KEY = env.str("SUNLIGHT_API_KEY")
GOOGLE_API_KEY = env.str("GOOGLE_MAP_API_KEY")
PROPUBLICA_API_KEY = env.str("PROPUBLICA_API_KEY", optional=True)


# Notification API Settings
NOTIFICATIONS_SOFT_DELETE = True
NOTIFICATIONS_USE_JSONFIELD = True


BASE_DIR = environ.Path(__file__)   # get root of the project

if env('DJANGO_HOST')==None :
    DJANGO_HOST = env.Str("DJANGO_HOST")
else:
    DJANGO_HOST = 'LOCALHOST'


# SSL Setup
if env(DJANGO_HOST)==None:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True



WSGI_APPLICATION = 'civiwiki.wsgi.application'


# Apex Contact for Production Errors
ADMINS = [('Development Team', 'dev@civiwiki.org')]


# AWS S3 Setup

public_root = BASE_DIR.path('public/')

if env('AWS_STORAGE_BUCKET_NAME')==None:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = public_root('media')
else:
    AWS_STORAGE_BUCKET_NAME = env.str("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_ACCESS_KEY_ID = env.str("AWS_S3_ACCESS_KEY_ID")
    AWS_S3_SECRET_ACCESS_KEY = env.str("AWS_S3_SECRET_ACCESS_KEY")
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    AWS_S3_SECURE_URLS = False
    AWS_QUERYSTRING_AUTH = False

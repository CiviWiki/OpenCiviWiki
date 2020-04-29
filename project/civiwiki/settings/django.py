"""
Django settings for civiwiki project.
Darius Calliet May 12, 2016
JDRanpariya April 29, 2020

Production settings file to select proper environment variables.
"""
import os
import dj_database_url
# django environ imported
import environ


BASE_DIR = environ.Path(__file__) - 2  # get root of the project



env = environ.Env()

# reading .env file
environ.Env.read_env(env_file=BASE_DIR('.env'))

env = environ.Env(DEBUG=(bool, False))

# Devlopment Environment Control
DEBUG = env("DEBUG")    # False if not in os.environ


# Raises django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = [".herokuapp.com", ".civiwiki.org", "127.0.0.1", "localhost", "0.0.0.0"]

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'storages',
    'channels',
    'civiwiki',
    'api',
    'rest_framework',
    'authentication',
    'frontend_views',
    'notifications',
    'corsheaders',
)

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)


CSRF_USE_SESSIONS = True  # Store the CSRF token in the users session instead of in a cookie

ROOT_URLCONF = 'civiwiki.urls'
LOGIN_URL = '/login'



#Frontend files
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "webapp/templates")],  # TODO: Add non-webapp template directory
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

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'webapp/static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Database
if env('CIVIWIKI_LOCAL_NAME')==None:
    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

    DATABASES = {
        'default': dj_database_url.parse(env.db("DATABASE_URL"))
    }
else:
    DATABASES = {
        'default': {
            'HOST': env.str('CIVIWIKI_LOCAL_DB_HOST', 'localhost'),
            'PORT': '5432',
            'NAME': env.str("CIVIWIKI_LOCAL_NAME"),
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'USER': env.str("CIVIWIKI_LOCAL_USERNAME"),
            'PASSWORD': env.str("CIVIWIKI_LOCAL_PASSWORD"),
        },
    }


# Email Backend Setup
if env('EMAIL_HOST')==None:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    EMAIL_HOST_USER = "test@civiwiki.org"
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = env.str("EMAIL_HOST")
    EMAIL_PORT = env.str("EMAIL_PORT")
    EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
    EMAIL_USE_SSL = True
    DEFAULT_FROM_EMAIL = EMAIL_HOST

    

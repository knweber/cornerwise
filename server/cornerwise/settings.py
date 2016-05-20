"""
Django settings for cornerwise project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
# For celery:
from celery.schedules import crontab
from datetime import timedelta

aodisnflkasfioanfoiafsdnio.wtf()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Determine if the app is in production mode by examining the
# environment variable set by Docker:
APP_MODE = os.environ.get("DJANGO_MODE", "development").lower()

#IS_PRODUCTION=(APP_MODE == "production")

# For now...
APP_MODE = "development"
IS_PRODUCTION = False

REDIS_HOST = os.environ.get("REDIS_HOST", "redis://")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

if "DJANGO_SECRET" in os.environ:
    SECRET_KEY = os.environ["DJANGO_SECRET"]
else:
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = '98yd3te&#$59^w!j(@b!@f8%fv49&p)vu+8)b4e5jcvfx_yeqs'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not IS_PRODUCTION

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'djcelery',
    'parcel',
    'proposal.ProposalConfig',
    'project.ProjectConfig',
    'user.UserAppConfig',
    'shared'
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

ROOT_URLCONF = 'cornerwise.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
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

WSGI_APPLICATION = 'cornerwise.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "")
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': POSTGRES_HOST,
        'NAME': 'postgres',
        'USER': 'postgres'
    },
    'migrate': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': POSTGRES_HOST,
        'NAME': 'postgres',
        'USER': 'postgres'
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

CACHES = {
    "default": {
        'BACKEND': 'redis_cache.RedisCache',
        "LOCATION": REDIS_HOST
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SERVER_DOMAIN = "cornerwise1125.cloudapp.net"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = 'static/'
MEDIA_URL = 'media/'

if not IS_PRODUCTION:
    STATIC_ROOT = '/client/'
    MEDIA_ROOT = '/media/'
else:
    STATIC_ROOT = os.environ.get("APP_STATIC_ROOT", "/client/")
    MEDIA_ROOT = os.environ.get("APP_MEDIA_ROOT", "/media/")

DOC_ROOT = os.path.join(MEDIA_ROOT, "doc")

BROKER_URL = REDIS_HOST

# Persist task results to the database
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'

CELERYBEAT_SCHEDULE = {
    "scrape-proposals": {
        "task": "proposal.fetch_proposals",
        # Run daily at midnight:
        "schedule": crontab(minute=0, hour=0)
    },

    "update-projects": {
        "task": "project.pull_updates",
        # Run on Mondays at midnight:
        "schedule": crontab(minute=0, hour=0, day_of_week="monday")
    },
}

CELERYD_TASK_SOFT_TIME_LIMIT = 60

GEO_BOUNDS = [42.371861543730496, -71.13338470458984,  # northwest
              42.40393908425197, -71.0679817199707]    # southeast

# The 'fit-width' of image thumbnails:
THUMBNAIL_DIM = (300, 300)

# String appended to addresses to assist geocoder:
GEO_REGION = "Somerville, MA"
GEOCODER = "arcgis"

# Email address and name for emails:
EMAIL_ADDRESS = "Cornerwise <cornerwise@somervillema.gov>"

AUTHENTICATION_BACKENDS = ["user.auth.TokenBackend"]

# Load select environment variables into settings:
for envvar in ["GOOGLE_API_KEY", "GOOGLE_STREET_VIEW_SECRET",
               "ARCGIS_CLIENT_ID", "ARCGIS_CLIENT_SECRET",
               "SOCRATA_APP_TOKEN", "SOCRATA_APP_SECRET"]:
    globals()[envvar] = os.environ.get(envvar, "")

try:
    # Allow user's local settings to shadow shared settings:
    from .local_settings import *
except ImportError as err:
    print("Could not find local_settings.py -- ", err)

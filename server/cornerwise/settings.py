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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Determine if the app is in production mode by examining the
# environment variable set by Docker:
APP_MODE = os.environ.get("DJANGO_MODE", "development").lower()

#IS_PRODUCTION=(APP_MODE == "production")

# For now...
APP_MODE = "development"
IS_PRODUCTION = False


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '98yd3te&#$59^w!j(@b!@f8%fv49&p)vu+8)b4e5jcvfx_yeqs'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'djcelery',
    'parcel',
    'proposal',
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
        'NAME': 'cornerwise',
        'USER': 'cornerwise'
    },
    'migrate': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': POSTGRES_HOST,
        'NAME': 'cornerwise',
        'USER': 'postgres'
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/client/'

if not IS_PRODUCTION:
    STATIC_ROOT = '/client'


# Celery configuration
BROKER_URL = os.environ.get("REDIS_HOST", "redis://")

## Persist task results to the database
CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'

from datetime import timedelta
CELERYBEAT_SCHEDULE = {
    "scrape-permits": {
        "task": "proposal.scrape_reports_and_decisions",
        "schedule": timedelta(days=1),
    }
}

ARCGIS_CLIENT_ID = "jYLY7AeA1U9xDiWu"
ARCGIS_CLIENT_SECRET = "64a66909ff724a0a9928838ef4462909"

try:
    # Allow user's local settings to shadow shared settings:
    from local_settings import *
except ImportError:
    pass

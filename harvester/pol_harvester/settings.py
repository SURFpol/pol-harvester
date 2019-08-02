"""
Django settings for pol_harvester project.

Generated by 'django-admin startproject' using Django 1.11.15.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Get git commit info to keep track of versions of data
GIT_COMMIT = os.environ.get('DJANGO_GIT_COMMIT', None)
if not GIT_COMMIT:
    raise ImproperlyConfigured('DJANGO_GIT_COMMIT variable has not been set to a git commit hash')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'm+2zzqoclh8b6um4%#k&(gw!!(=mmw&$y&u^14jkyt$t==p-$e')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get('DJANGO_DEBUG', False)))

ALLOWED_HOSTS = [
    'localhost',
    '.surfpol.nl'
]
CORS_ORIGIN_WHITELIST = [
    'localhost:8080',
    'localhost:8000',
    '127.0.0.1:8080',
    'pol-tagger.dev.swarm.surfedu.nl'
]
SITE_ID = 1


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django.contrib.sites',
    'django.contrib.sitemaps',

    'datagrowth',
    'pol_harvester',
    'edurep',
    'ims',
    'surfshare',
    'search',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'pol_harvester.authentication.SearchBasicAuthMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pol_harvester.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'pol_harvester.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pol',
        'USER': 'django',
        'PASSWORD': os.environ.get('DJANGO_POSTGRES_PASSWORD', 'Yd36ewNjYBKY4MRUjmXMpaoHvxvR2Yqe'),
        'HOST': os.environ.get('POSTGRES_HOST', '127.0.0.1')
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Basic Auth
# https://github.com/hirokiky/django-basicauth

username = os.environ.get("ELASTIC_SEARCH_USERNAME")
password = os.environ.get("ELASTIC_SEARCH_PASSWORD")
if not username or not password:
    raise ImproperlyConfigured("Username and/or password not specified for Basic Auth")
BASICAUTH_USERS = {
    username: password
}


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Logging
# https://docs.djangoproject.com/en/1.11/topics/logging/

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'debug_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/pol_harvester/logs/debug.log',
        },
        'freeze_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/pol_harvester/logs/freeze.log',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        'pol_harvester': {
            'handlers': ['debug_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'freeze': {
            'handlers': ['freeze_file'],
            'level': 'INFO',
            'propagate': True,
        },
        'datagrowth.command': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        }
    },
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/'
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'statics')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "..", "rateapp", "dist"),
]
# We're serving static files through Whitenoise
# See: http://whitenoise.evans.io/en/stable/index.html#
# If you doubt this decision then read the "infrequently asked question" section for details
WHITENOISE_INDEX_FILE = 'index.html'
if DEBUG:
    WHITENOISE_AUTOREFRESH = True
    WHITENOISE_USE_FINDERS = True

MEDIA_ROOT = os.path.join('..', 'media')

SESSION_COOKIE_PATH = '/admin/'


# Rest framework
# https://www.django-rest-framework.org/

REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}


# Datagrowth
# https://github.com/fako/datascope/blob/master/datagrowth/settings.py

DATAGROWTH_DATA_DIR = os.path.join('..', 'data')
DATAGROWTH_REQUESTS_PROXIES = None
DATAGROWTH_REQUESTS_VERIFY = True
DATAGROWTH_DATETIME_FORMAT = "%Y%m%d%H%M%S%f"

DATAGROWTH_KALDI_BASE_PATH = '/home/surf/kaldi'
DATAGROWTH_KALDI_ASPIRE_BASE_PATH = '/home/surf/kaldi/egs/aspire/s5'
DATAGROWTH_KALDI_NL_BASE_PATH = '/home/surf/Kaldi_NL'

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GOOGLE_CX = os.environ.get("GOOGLE_CX")
MAX_BATCH_SIZE = 500


# Elastic Search

ELASTIC_SEARCH_USERNAME = os.environ.get("ELASTIC_SEARCH_USERNAME", None)
ELASTIC_SEARCH_PASSWORD = os.environ.get("ELASTIC_SEARCH_PASSWORD", None)
ELASTIC_SEARCH_URL = os.environ.get("ELASTIC_SEARCH_URL", "https://surfpol.sda.surf-hosted.nl")
ELASTIC_SEARCH_HOST = os.environ.get("ELASTIC_SEARCH_HOST", "surfpol.sda.surf-hosted.nl")
ELASTIC_SEARCH_ANALYSERS = {
    'en': 'english',
    'nl': 'dutch'
}


# Project Open Leermaterialen

HUMANIZED_MIME_TYPES = {
    'unknown': 'unknown',
    'application/pdf': 'pdf',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'powerpoint',
    'application/vnd.ms-powerpoint': 'powerpoint',
    'application/msword': 'word',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'word',
    'application/rtf': 'word',
    'text/plain': 'word',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'excel',
    'text/html': 'html',
    'application/xhtml+xml': 'html',
    'video/flv': 'video',
    'video/x-flv': 'video',
    'video': 'video',
    'image': 'image',
    'application/zip': 'zip',
    'audio/mpeg': 'audio',
    'application/octet-stream': 'other'
}

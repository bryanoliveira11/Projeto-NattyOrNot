"""
Django settings for NattyOrNot project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from datetime import timedelta
from os import environ
from pathlib import Path
from typing import List

from django.contrib.messages import constants
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environ.get('SECRET_KEY', 'INSECURE')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if environ.get('DEBUG') == '0' else True

ALLOWED_HOSTS: List = [environ.get('RECAPTCHA_DOMAIN', '')]

CSRF_TRUSTED_ORIGINS: List = [environ.get(
    'CSRF_TRUSTED_ORIGINS', '')
]

# Application definition

INSTALLED_APPS = [
    # my apps
    'users',
    'training',
    # django defaults
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # cors headers
    'corsheaders',
    # rest framework
    'rest_framework',
    # all auth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # debug toolbar
    'debug_toolbar',
    # axes
    'axes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # cors headers middleware
    'corsheaders.middleware.CorsMiddleware',
    # all auth middleware
    'allauth.account.middleware.AccountMiddleware',
    # debug toolbar middleware
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # AxesMiddleware should be the last middleware in the MIDDLEWARE list.
    'axes.middleware.AxesMiddleware',
]

ROOT_URLCONF = 'NattyOrNot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'base_templates'],
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

WSGI_APPLICATION = 'NattyOrNot.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': environ.get('DATABASE_ENGINE'),
        'NAME': environ.get('DATABASE_NAME'),
        'USER': environ.get('DATABASE_USER'),
        'PASSWORD': environ.get('DATABASE_PASSWORD'),
        'HOST': environ.get('DATABASE_HOST'),
        'PORT': environ.get('DATABASE_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'pt-BR'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'base_static']
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# tags que serão usadas no css para estilizar as mensagens ao usuário
MESSAGE_TAGS = {
    constants.DEBUG: 'message-debug',
    constants.ERROR: 'message-error',
    constants.SUCCESS: 'message-success',
    constants.INFO: 'message-info',
    constants.WARNING: 'message-warning',
}


# django axes config
AXES_ENABLED = False if environ.get('AXES_ENABLED') == '0' else True
AXES_LOCKOUT_CALLABLE = "users.views.user_lockout.lockout"
AXES_COOLOFF_TIME = timedelta(minutes=15)
AXES_FAILURE_LIMIT = 5
AXES_LOCKOUT_PARAMETERS = [["username"]]

AUTHENTICATION_BACKENDS = [
    # AxesStandaloneBackend should be the first backend in the AUTHENTICATION_BACKENDS list.
    'axes.backends.AxesStandaloneBackend',
    # Django ModelBackend is the default authentication backend.
    'django.contrib.auth.backends.ModelBackend',
    # all auth backend
    'allauth.account.auth_backends.AuthenticationBackend'
]


# django debug toolbar config

INTERNAL_IPS = [
    '127.0.0.1',
]

# all auth site id
SITE_ID = int(environ.get('SITE_ID', 2))

# all auth configs

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

SOCIALACCOUNT_LOGIN_ON_GET = True

ACCOUNT_DEFAULT_HTTP_PROTOCOL = environ.get(
    'ACCOUNT_DEFAULT_HTTP_PROTOCOL', 'https'
)

LOGIN_REDIRECT_URL = "/"


# django rest api
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,  # elements per page
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

# jwt token
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "BLACKLIST_AFTER_ROTATION": False,
    "SIGNING_KEY": environ.get('SECRET_KEY_JWT', 'INSECURE'),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

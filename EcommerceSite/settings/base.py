"""
Django settings for EcommerceSite project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os, sys
# from pathlib import Path


#setting ---------------------------------------------------------
from unipath import Path
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_DIR = Path(__file__).ancestor(3)
PROJECT_APPS = Path(__file__).ancestor(2)

sys.path.insert(0, Path(PROJECT_APPS, 'apps'))
#------------------------------------------------------------------


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-47r26=nuyq(84*gg!+5%%ip(qee4x-ffl#us0-89-b5^+b$8&q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'paypal.standard.ipn'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'EcommerceSite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [PROJECT_APPS.child("templates"),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        # 'libraries':{
        #     'custom_templatetag': 'EcommerceSite.templatetags.cart',

        #     }
        },
    },
]

WSGI_APPLICATION = 'EcommerceSite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


DATABASES = {
  'default': {
      'ENGINE':   'django.db.backends.postgresql',
      'NAME':     'ecommerce',
      'USER':     'postgres',
      'PASSWORD': 'postgres',
      'HOST':     'localhost',
      'PORT':     5432,
  }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

MEDIA_ROOT = PROJECT_APPS.child('media')

MEDIA_URL = '/media/'


# Static files (CSS, JavaScript, Images, Pdf)
# STATIC_ROOT = PROJECT_APPS.child('static')

STATICFILES_DIRS = [
   PROJECT_APPS.child("static")
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'core.User'

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_PORT = 587
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'shubham.thoughtwin@gmail.com'
# EMAIL_HOST_PASSWORD = 'osfapvbgpeneopid'

DEFAULT_FROM_EMAIL='noreply@postyourcars.com'
FROM_EMAIL='noreply@postyourcars.com'
EMAIL_HOST='email-smtp.us-east-2.amazonaws.com'
EMAIL_HOST_USER='AKIAZY4LX5J6EY7PGHOS'
EMAIL_HOST_PASSWORD='BOA8LJdyGOzZrLcl3PcyCkh1aSpsRmEBOKmcmXvdew+i'
# DEFAULT_FROM_EMAIL = 'shubham.thoughtwin@gmail.com'


API_KEY="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"

LOGOUT_REDIRECT_URL = 'home/'

PAYPAL_RECEIVER_EMAIL = 'youremail@mail.com'

PAYPAL_TEST = True


PAYPAL_CLIENT_ID = "ASILJdz-nMq6J9xxFYdCn37J7fsV-ibbnw10NWJaI9JgXtjTEPojrMB5_wnKwqd5Z6BG4Hf7qqig2u9e"
PAYPAL_SECRET_KEY = "EMUweYiU8M2g749qAHPpjzCAFJ2eFmyY_6SLjtEFfXT4uKRkcf_mSai53nJp0aJJ7Pc7i5w6j6_edDXp"

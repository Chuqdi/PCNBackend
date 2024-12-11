"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import environ
env = environ.Env()
environ.Env.read_env()

import os
from pathlib import Path
import firebase_admin
from firebase_admin import credentials
import dj_database_url



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*lciycldl&*+8&a!np3dx5u#z@ekuhxg6v9x0_^8-tqlx#%2u^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    "storages",
    'django.contrib.staticfiles',
    "rest_framework",
    'django_celery_beat',
    'django_celery_results',
    "corsheaders",
    "rest_framework.authtoken",
    
    "users",
    "PCNs",
    "vehicles",
    "subscriptions",
    "discount_codes",
    "subscription_email"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR.joinpath("templates")],
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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases



DATABASES = {
    'default': dj_database_url.config(
        default="postgresql://pcn_user:mhiWylYlRG6Lj1JtejcuKinePKkKBgdW@dpg-ct8rr223esus7385o1v0-a.oregon-postgres.render.com/pcn",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# DATABASES = {
# 'default': {
#     'ENGINE': 'django.db.backends.postgresql_psycopg2',
#     'NAME': "pcn", 
#     'USER': "pcn_user",
#     'PASSWORD':"mhiWylYlRG6Lj1JtejcuKinePKkKBgdW",
#     'HOST':"dpg-ct8rr223esus7385o1v0-a.oregon-postgres.render.com", 
#     'PORT': "5432",
# },
#  'default1': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],

    'DEFAULT_PAGINATION_CLASS':
    'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field





DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOW_ALL_ORIGINS = True

AUTH_USER_MODEL = "users.User"
# STRIPE_SECRET_KEY ="sk_test_51NuLgnA3T5bTc4ZwW0aZ1bDOtqg7ciR0CfKfTnRqJBBiy3aPiXChQNPt596pD8Ybj4qpB8MFxFawzDI2Rr5y536F00zbCPnjce"

STRIPE_SECRET_KEY ="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"




# CELERY_BROKER_URL = "rediss://default:AVNS_kobLCmjKB15OTYSSnpr@db-redis-nyc3-24025-do-user-16518620-0.c.db.ondigitalocean.com:25061"
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['pickle', 'application/json']
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_TASK_SELERLIZER = 'pickle'
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'UTC'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_IMPORTS = ("utils",)





EMAIL_HOST = "smtp.mailgun.org"
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_PORT = 465
DEFAULT_FROM_EMAIL = "PCNTicket<support@usepcn.com>"
EMAIL_HOST_USER = "support@usepcn.com"
EMAIL_HOST_PASSWORD ="gODFATHERTINZ1@"



# AWS CONFIGURATIONS
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_ACCESS_KEY_ID = "AKIAQXZDR553VZ447CO4"
AWS_SECRET_ACCESS_KEY = "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"
AWS_DEFAULT_ACL = None
AWS_STORAGE_BUCKET_NAME = "pcnticket1"
AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
AWS_LOCATION = "static"
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"



cred = credentials.Certificate(BASE_DIR.joinpath("pcnticket-de55b-firebase-adminsdk-2trso-e60c2a092d.json"))
firebase_admin.initialize_app(cred)


REFERAL_CREDIT_AMOUNT = 5
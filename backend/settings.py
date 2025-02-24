"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
from dotenv import load_dotenv
import os
from pathlib import Path
import firebase_admin
from firebase_admin import credentials
import dj_database_url



load_dotenv()

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
    "subscription_email",
    "virualcards",
    "user_notifications"
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
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# DATABASES = {
#  'default': {
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
STRIPE_SECRET_KEY =os.getenv("STRIPE_SECRET_KEY")
# STRIPE_SECRET_KEY ="sk_test_51NNZ6uEaYyTuzzYV1M0nLvkxHLyEGR1d91FcfcmLZ0LVZNuTkm43ergE8ryGniufmRS4jmT1U9cM1jhK8pFucFmI00vew8ccdG"


STRIPE_WEBHOOK_SECRET =os.getenv("STRIPE_WEBHOOK_SECRET")
# STRIPE_WEBHOOK_SECRET ="whsec_nOGSPmEZ34vcGJbkT94xw2YPAgDkNymz"

CELERY_BROKER_URL = os.getenv("REDIS_URL")
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['pickle', 'application/json']
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_TASK_SELERLIZER = 'pickle'
CELERY_ENABLE_UTC = True
# CELERY_TIMEZONE = 'UTC'
CELERY_TIMEZONE = 'Africa/Lagos'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_IMPORTS = ("utils",)





EMAIL_HOST = "smtp.mailgun.org"
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_PORT = 465
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")



# AWS CONFIGURATIONS
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY =os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_ACL = None
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
AWS_LOCATION = "static"
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"



firebase_creds = credentials.Certificate({
    "type": os.getenv("FIREBASE_TYPE"),
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id":os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri":os.getenv("FIREBASE_AUTH_URI"),
    "token_uri":os.getenv("FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("FIREBASE_UNIVERSE_DOMAIN"),
})

firebase_admin.initialize_app(firebase_creds)


REFERAL_CREDIT_AMOUNT = 5


STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
    },
}
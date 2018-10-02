"""
Django settings for coursera_dashboard project.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

FRONTEND_URL = os.environ.get("DASHIT_FRONTEND_URL", "http://localhost:8080/#/")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = ["coursera.apps.CourseraConfig", "rest_framework"]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "oauth2_provider.middleware.OAuth2TokenMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "coursera_dashboard.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "debug": DEBUG,
        },
    }
]

WSGI_APPLICATION = "coursera_dashboard.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {"default": dj_database_url.config()}

DATABASE_ROUTERS = ["coursera_dashboard.db_router.DatabaseRouter"]

AUTHENTICATION_BACKENDS = ["auth.backends.OAuth2Backend"]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Allow all host headers
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "dashit.win.tue.nl"]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.environ.get("DJANGO_STATIC_ROOT")

MEDIA_ROOT = os.environ.get("DJANGO_MEDIA_ROOT")

# Extra places for collectstatic to find static files.
# STATICFILES_DIRS = [os.path.join(PROJECT_ROOT, "static")]

CORS_ORIGIN_WHITELIST = ["localhost:8080", "cornytrace.github.io"]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
    )
}

# EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

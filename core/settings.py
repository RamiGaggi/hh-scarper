import os
from pathlib import Path

import dj_database_url
import nltk
from django.core.management.utils import get_random_secret_key

nltk.download('stopwords', quiet=True)


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv('DATABASE_URL', get_random_secret_key())


DEBUG = os.getenv('DEBUG', 'False').lower() in {'yes', '1', 'true'}


ALLOWED_HOSTS = ['localhost', '.herokuapp.com']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hhscarper',
    'bootstrap4',
    'django_extensions',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'core.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ],
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


WSGI_APPLICATION = 'core.wsgi.application'


CONN_MAX_AGE = 600

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}

DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    DATABASES['default'] = dj_database_url.parse(
        os.getenv('DATABASE_URL'),
        conn_max_age=CONN_MAX_AGE,
    )


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


LANGUAGE_CODE = 'ru-ru'

LANGUAGES = [
    ('ru', 'Russian'),
    ('en', 'English'),
]

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': BASE_DIR / 'logs/task_manager.log',
            'formatter': 'verbose',
            'interval': 1,
            'backupCount': 7,
            'when': 'D',
        },
        'console': {
            'level': os.getenv('LOG_LEVEL', 'INFO'),
            'formatter': 'simple',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'level': os.getenv('LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'django.utils': {
            'level': 'INFO',
        },
        'django.db.backends': {
        'level': 'INFO',
        },
    },
}

AUTH_USER_MODEL = 'hhscarper.User'


CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379')

CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

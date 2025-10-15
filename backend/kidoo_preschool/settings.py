"""
Django settings for kidoo_preschool project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Try to load from .env, but provide defaults if it fails
try:
    from decouple import config
    SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production-kidoo-preschool-2024')
    DEBUG = config('DEBUG', default=True, cast=bool)
    
    # Database configuration from environment variables
    DB_HOST = config('DB_HOST', default='localhost')
    DB_PORT = config('DB_PORT', default='1433')
    DB_NAME = config('DB_NAME', default='KIDOO')
    DB_USER = config('DB_USER', default='')
    DB_PASSWORD = config('DB_PASSWORD', default='')
    USE_SQLSERVER = config('USE_SQLSERVER', default=False, cast=bool)
except:
    SECRET_KEY = 'django-insecure-change-this-in-production-kidoo-preschool-2024'
    DEBUG = True
    DB_HOST = 'localhost'
    DB_PORT = '1433'
    DB_NAME = 'KIDOO'
    DB_USER = ''
    DB_PASSWORD = ''
    USE_SQLSERVER = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'django_filters',
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kidoo_preschool.urls'

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

WSGI_APPLICATION = 'kidoo_preschool.wsgi.application'

# Database
if USE_SQLSERVER:
    DATABASES = {
        'default': {
            'ENGINE': 'mssql',
            'NAME': 'KIDOO',               # Database name
            'USER': '',               # SQL Server username
            'PASSWORD': '',       # SQL Server password
            'HOST': 'localhost\\SQLEXPRESS',               # e.g., 'localhost\\SQLEXPRESS'
            'PORT': '',                    # Leave empty for named instances
            'OPTIONS': {
                'driver': 'SQL Server Native Client 11.0',  # Make sure this driver is installed
                'extra_params': 'Trusted_Connection=yes;Server=localhost\\SQLEXPRESS;Database=KIDOO;'
            },
        },
        'sqlite': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True

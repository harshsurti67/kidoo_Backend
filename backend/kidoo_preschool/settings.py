# """
# Django settings for kidoo_preschool project.
# """

# from pathlib import Path
# import os

# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent

# # Try to load from .env, but provide defaults if it fails
# try:
#     from decouple import config
#     SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production-kidoo-preschool-2024')
#     DEBUG = config('DEBUG', default=True, cast=bool)
    
#     # Database configuration from environment variables
#     DB_HOST = config('DB_HOST', default='dpg-d3nkd8ruibrs738g02p0-a')
#     DB_PORT = config('DB_PORT', default='5432')
#     DB_NAME = config('DB_NAME', default='kidoo')
#     DB_USER = config('DB_USER', default='kidoo_user')
#     DB_PASSWORD = config('DB_PASSWORD', default='')
#     USE_POSTGRESQL = config('USE_POSTGRESQL', default=False, cast=bool)
# except:
#     SECRET_KEY = 'django-insecure-change-this-in-production-kidoo-preschool-2024'
#     DEBUG = True
#     DB_HOST = 'dpg-d3nkd8ruibrs738g02p0-a'
#     DB_PORT = '5432'
#     DB_NAME = 'kidoo'
#     DB_USER = 'kidoo_user'
#     DB_PASSWORD = ''
#     USE_POSTGRESQL = False

# ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0','https://kidoo-backend-6.onrender.com']

# # Application definition
# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'rest_framework',
#     'corsheaders',
#     'django_filters',
#     'api',
# ]

# MIDDLEWARE = [
#     'corsheaders.middleware.CorsMiddleware',
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'kidoo_preschool.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'kidoo_preschool.wsgi.application'

# # Database
#  DATABASES = {
#       'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': BASE_DIR / 'db.sqlite3',
#         }
#     }

# # if USE_POSTGRESQL:
# #       DATABASES = {
# #     'default': {
# #         'ENGINE': 'django.db.backends.postgresql',
# #         'NAME': 'kidoo',
# #         'USER': 'kidoo_user',
# #         'PASSWORD': 'your-postgres-password-here',
# #         'HOST': 'dpg-d3nkd8ruibrs738g02p0-a',
# #         'PORT': '5432',
# #     }
# # }

#     # DATABASES = {
#     #     'default': {
#     #         'ENGINE': 'mssql',
#     #         'NAME': 'KIDOO',               # Database name
#     #         'USER': '',               # SQL Server username
#     #         'PASSWORD': '',       # SQL Server password
#     #         'HOST': 'localhost\\SQLEXPRESS',               # e.g., 'localhost\\SQLEXPRESS'
#     #         'PORT': '',                    # Leave empty for named instances
#     #         'OPTIONS': {
#     #             'driver': 'SQL Server Native Client 11.0',  # Make sure this driver is installed
#     #             'extra_params': 'Trusted_Connection=yes;Server=localhost\\SQLEXPRESS;Database=KIDOO;'
#     #         },
#     #     },
#     #     'sqlite': {
#     #         'ENGINE': 'django.db.backends.sqlite3',
#     #         'NAME': BASE_DIR / 'db.sqlite3',
#     #     }
#     # }
    
# # Password validation
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]

# # Internationalization
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_TZ = True

# # Static files (CSS, JavaScript, Images)
# STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR / 'staticfiles'

# # Media files
# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'

# # Default primary key field type
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # REST Framework settings
# REST_FRAMEWORK = {
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
#     'PAGE_SIZE': 20,
#     'DEFAULT_FILTER_BACKENDS': [
#         'django_filters.rest_framework.DjangoFilterBackend',
#         'rest_framework.filters.SearchFilter',
#         'rest_framework.filters.OrderingFilter',
#     ],
# }

# # CORS settings
# CORS_ALLOWED_ORIGINS = [
#     'https://kidoostatic.vercel.app', 
#     "http://localhost:3000",
#     "http://127.0.0.1:3000",
# ]

# CORS_ALLOW_CREDENTIALS = True
"""
Django settings for kidoo_preschool project.
Unified settings using SQLite for all environments.
Includes CORS, CSRF, WhiteNoise, and email configuration.
"""

from pathlib import Path
import os
import cloudinary
try:
    import dj_database_url  # type: ignore
except Exception:
    dj_database_url = None  # Fallback if library not installed locally

# -----------------------------
# BASE DIR
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# SECRET KEY & DEBUG
# -----------------------------
try:
    from decouple import config
    SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production-kidoo-preschool-2024')
    DEBUG = config('DEBUG', default=False, cast=bool)
except ImportError:
    SECRET_KEY = 'django-insecure-change-this-in-production-kidoo-preschool-2024'
    DEBUG = False

# -----------------------------
# ALLOWED HOSTS
# -----------------------------
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    'kidoo-backend-6.onrender.com',  # your Render.com backend URL
]

# -----------------------------
# CSRF / CORS
# -----------------------------
CSRF_TRUSTED_ORIGINS = ['https://kidoostatic.vercel.app']
CORS_ALLOWED_ORIGINS = [
    'https://kidoostatic.vercel.app', 
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True

# -----------------------------
# INSTALLED APPS
# -----------------------------
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
    'cloudinary',
    'cloudinary_storage',
]
"""Cloudinary configuration (hardcoded, per user request)
WARNING: Secrets are embedded in source. Prefer environment variables in production.
"""
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'diadyznqa',
    'API_KEY': '643916278533495',
    'API_SECRET': 'mljiWucEv3eiH6wFlj2aJ2_M0lY',
    # Allow uploading images, videos, and other asset types
    'RESOURCE_TYPE': 'auto',
}

# Ensure Cloudinary SDK is configured (some libs read directly from cloudinary.config)
cloudinary.config(
    cloud_name=CLOUDINARY_STORAGE['CLOUD_NAME'],
    api_key=CLOUDINARY_STORAGE['API_KEY'],
    api_secret=CLOUDINARY_STORAGE['API_SECRET']
)

# -----------------------------
# MIDDLEWARE
# -----------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # serve static files
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

# -----------------------------
# DATABASE (SQLite by default; auto-switch to PostgreSQL if DATABASE_URL set)
# -----------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# If running on Render with PostgreSQL, use DATABASE_URL
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL and dj_database_url:
    # conn_max_age keeps connections persistent; ssl required by Render
    DATABASES['default'] = dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        ssl_require=True,
    )

# -----------------------------
# PASSWORD VALIDATION
# -----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# -----------------------------
# INTERNATIONALIZATION
# -----------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# -----------------------------
# STATIC & MEDIA
# -----------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# -----------------------------
# REST FRAMEWORK
# -----------------------------
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# -----------------------------
# SESSION
# -----------------------------
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# -----------------------------
# EMAIL SETTINGS
# -----------------------------
try:
    from decouple import config
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
    EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
    DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@kidoopreschool.com')
except:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = 'noreply@kidoopreschool.com'

# -----------------------------
# DEFAULT PK FIELD
# -----------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

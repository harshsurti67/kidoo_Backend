"""
Free hosting settings for kidoo_preschool project.
Optimized for Render, Railway, and other free hosting platforms.
"""

from .settings import *
import os
import dj_database_url
from decouple import config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Security settings
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production-kidoo-preschool-2024')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='kidoo-backend-5.onrender.com,localhost,127.0.0.1').split(',')

# Database - Use SQL Server for free hosting
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': config('DB_NAME', default='KIDOO'),
        'USER': config('DB_USER', default=''),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='localhost\\SQLEXPRESS'),
        'PORT': config('DB_PORT', default=''),
        'OPTIONS': {
            'driver': 'SQL Server Native Client 11.0',
            'extra_params': 'Trusted_Connection=yes;Server=localhost\\SQLEXPRESS;Database=KIDOO;'
        },
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For serving static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HTTPS settings (uncomment when you have SSL)
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# CORS settings for free hosting
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='').split(',')
CORS_ALLOW_CREDENTIALS = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Email settings (configure for your email service)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@kidoopreschool.com')

# WhiteNoise configuration for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Session settings
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

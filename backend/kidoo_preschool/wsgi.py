"""
WSGI config for kidoo_preschool project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kidoo_preschool.settings')

application = get_wsgi_application()

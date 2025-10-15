#!/usr/bin/env bash
# Build script for Render.com deployment

# Install dependencies
pip install -r backend/requirements_render.txt

# Run migrations
python backend/manage.py migrate --noinput

# Collect static files
python backend/manage.py collectstatic --noinput

# Create superuser (optional - you can do this manually later)
# python backend/manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" || true

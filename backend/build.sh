#!/usr/bin/env bash
# Build script for Render.com deployment

# Install dependencies
pip install -r requirements_simple.txt

# Change to backend directory
cd backend

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Create superuser (optional - you can do this manually later)
# python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" || true

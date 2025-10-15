#!/usr/bin/env bash
# Build script for Render.com deployment

set -euo pipefail

# Always run from this script's directory (the backend folder)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Install dependencies (includes Cloudinary packages)
pip install -r requirements_render.txt

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Create superuser (optional - you can do this manually later)
# python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" || true

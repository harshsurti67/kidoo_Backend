#!/usr/bin/env bash
# Build script for Render.com deployment

# Install dependencies
pip install -r requirements.txt

# Change to backend directory and run migrations
cd backend
python manage.py migrate --noinput
python manage.py collectstatic --noinput

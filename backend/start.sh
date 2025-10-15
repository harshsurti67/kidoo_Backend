#!/usr/bin/env bash
# Start script for Render.com deployment

# Change to backend directory
cd backend

# Set Django settings module
export DJANGO_SETTINGS_MODULE=kidoo_preschool.settings_production

# Start the application
exec gunicorn kidoo_preschool.wsgi:application --bind 0.0.0.0:$PORT

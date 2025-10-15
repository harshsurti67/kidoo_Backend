#!/usr/bin/env bash
cd backend
export DJANGO_SETTINGS_MODULE=kidoo_preschool.settings_production
exec gunicorn kidoo_preschool.wsgi:application --bind 0.0.0.0:$PORT

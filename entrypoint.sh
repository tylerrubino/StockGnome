#!/bin/bash

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start the app
gunicorn main.wsgi:application --bind 0.0.0.0:80
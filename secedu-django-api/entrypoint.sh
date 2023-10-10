#!/bin/sh
python manage.py migrate
python manage.py makemigrations --noinput 
python manage.py migrate --noinput 
python manage.py collectstatic --noinput 
gunicorn --workers=1 --timeout=3600 --bind=0.0.0.0:9000 core.wsgi:application
exec "$@"

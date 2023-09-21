#!/bin/sh

#python manage.py makemigrations

python manage.py migrate --no-input

python manage.py collectstatic --no-input

#python setup.py --no-input

gunicorn core.wsgi:application --bind 0.0.0.0:9000

#!/bin/sh
python manage.py migrate --no-input

python setup.py --no-input

python manage.py makemigrations

python manage.py collectstatic --no-input

gunicorn core.wsgi:application --bind 0.0.0.0:9000

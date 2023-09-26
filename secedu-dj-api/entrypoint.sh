#!/bin/sh
python manage.py makemigrations 
python manage.py migrate 
python manage.py collectstatic 
python setup.py
gunicorn core.wsgi:application --bind 0.0.0.0:9000

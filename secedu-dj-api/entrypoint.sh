#!/bin/bash -x

#Script para makemigrations e migrate do Django
# Autor: Edson Lourenço
# Data: 20/01/2021

python manage.py makemigrations --noinput || exit 1
exec "$@"

python setup.py --noinput || exit 1
exec "$@"

python manage.py migrate --noinput || exit 1
exec "$@"

python manage.py runserver 0.0.0.0:8000
#gunicorn --workers=1 --timeout=3600 --bind=0.0.0.0:8000 core.wsgi
exec "$@"

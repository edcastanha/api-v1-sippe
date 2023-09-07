#!/bin/bash

#Script para makemigrations e migrate do Django
# Autor: Edson Lourenço
# Data: 20/01/2021

#Intall wait-for-it

wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh \
-O /usr/local/bin/wait-for-it && \
chmod +x /usr/local/bin/wait-for-it

/usr/local/bin/wait-for-it -t 0 postgres-api:5432 -- echo "Iniciando Makemigrations e Migrate"

#gunicorn --workers=1 --timeout=3600 --bind=0.0.0.0:5000 "app:create_app()"

python manage.py migrate --noinput || exit 1
exec "$@"

python manage.py makemigrations --noinput || exit 1
exec "$@"

python setup.py --noinput || exit 1
exec "$@"

python manage.py migrate --noinput || exit 1
exec "$@"

python manage.py runserver 0.0.0.0:8000 
exec "$@"

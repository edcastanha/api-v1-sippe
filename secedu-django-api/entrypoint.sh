#!/bin/sh
# python manage.py flush --no-input

echo "Aplicando >>> Migrate 1"
python manage.py migrate

echo "Aplicando >>> Create superuser"
python setup.py

echo "Aplicando >>> Makemigrations"
python manage.py makemigrations

echo "Aplicando >>> Migrate 2"
python manage.py migrate

echo "Aplicando >>> Collectstatic"
python manage.py collectstatic --no-input

exec "$@"

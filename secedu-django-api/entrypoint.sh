#!/bin/sh
echo "Apply Migrate"
python manage.py migrate
exec "$@"
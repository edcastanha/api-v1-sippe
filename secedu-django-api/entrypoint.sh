#!/bin/ash
echo "Apply Migrate"
python manage.py migrate
exec "$@"
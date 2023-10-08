#!/bin/sh

set -o errexit
set -o pipefail
set -o nounset

# python manage.py flush --no-input
echo "Apply Migrate"
python manage.py migrate
echo "Apply Collectstatic"
python manage.py collectstatic --no-input --clear

exec "$@"

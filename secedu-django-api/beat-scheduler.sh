#!/bin/sh
echo "Aplicações de BEAT"
celery -A core beat --loglevel=INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
exec "$@"
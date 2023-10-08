#!/bin/sh

echo "Apply BEAT"
celery -A core beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler

exec "$@"
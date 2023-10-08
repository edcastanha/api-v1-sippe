#!/bin/sh
echo "Apply WORKER"
celery -A core worker -l info
exec "$@"
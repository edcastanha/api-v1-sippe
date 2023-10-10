#!/bin/sh
echo "Aplicados WORKER"
celery -A core worker --loglevel=INFO
exec "$@"
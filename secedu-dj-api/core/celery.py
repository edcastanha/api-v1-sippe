from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(
    result_expires=3600,
    broker_url = 'amqp://secedu:ep4X1!br@secedu-rmq-task:5672/',
    timezone = 'America/Sao_Paulo',
    queue_name_prefix = 'secedu-task',
    exchange = 'secedu',
)

app.autodiscover_tasks()

def debug_task(self):
    print(f'Request: {self.request!r}')

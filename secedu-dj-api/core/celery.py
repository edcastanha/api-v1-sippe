from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core',
             include=[
                'core.cameras.tasks',
                'core.cadastros.tasks',
            ]
        )

app.config_from_object('django.conf:settings', namespace='CELERY')

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
    callback='start_consumer_path',
)

app.autodiscover_tasks()

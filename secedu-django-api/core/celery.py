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

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

app.autodiscover_tasks()

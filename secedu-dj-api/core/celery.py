import os

from celery import Celery

## pass the settings module to the celery program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

## create the celery app instance
app = Celery('core')

## adicione o módulo de configurações do django como fonte de 
# configuração para o celery i.e. configurar o celery diretamente 
# a partir do django settings  a configuração do celery é 
# especificada usando CELERY em letras maiúsculas
app.config_from_object('django.conf:settings', namespace='CELERY')

## o celery irá descobrir automaticamente tarefas de todas as 
# aplicações instaladas no nosso projeto django seguindo a 
# convenção tasks.py
app.autodiscover_tasks()

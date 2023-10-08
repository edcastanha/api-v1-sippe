from django.conf import settings
from core.cadastros.models import Aluno
from core.loggingMe import logger
from celery import shared_task
from time import sleep
from celery.utils.log import get_task_logger
from django.core.management import call_command

logger = get_task_logger(__name__)

@shared_task()
def send_email(email, name):
    print(f'send_email: {email} - nome: {name}')

# tasks.py
from celery import shared_task
from datetime import datetime

from core.cameras.models import Cameras
from core.loggingMe import logger
from core.celery import app
from .producer import ProducerCameras

EXCHANGE = 'secedu'
QUEUE_PUBLISHIR = 'embedding'
ROUTE_KEY = 'verification'


@shared_task(name='producer task path')
def start_producerr_path():
    start = ProducerCameras()
    start.start_run()
    
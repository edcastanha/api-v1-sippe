from celery import shared_task
import os
import re
import json
from datetime import datetime
import pika

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
    start.process_message()
    logger.info(f'<**_start_producerr_path_**> ProducerCameras.process_message')
    
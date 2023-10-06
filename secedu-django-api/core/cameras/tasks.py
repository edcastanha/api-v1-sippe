from celery import shared_task
import os
import re
import json
from datetime import datetime
import pika

from core.cameras.models import Cameras
from core.loggingMe import logger
from core.publisher import Publisher
from core.celery import app
from core.producer import ProducerCameras

EXCHANGE = 'secedu'
QUEUE_PUBLISHIR = 'embedding'
ROUTE_KEY = 'verification'


@shared_task(name='core.cameras.tasks.start_consumer_path' ,
             exchange='secedu')
def start_consumer_path():
    start = ProducerCameras()
    start.process_message()
    logger.info(f' <**_ 4 _**> ConsumerPath: start_consumer_path . process_message')
    
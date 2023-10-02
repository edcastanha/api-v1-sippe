from __future__ import absolute_import, unicode_literals
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

QUEUE_PUBLISHIR = 'embedding'
EXCHANGE = 'secedu'
ROUTE_KEY = 'verification'

FTP_PATH = 'ftp'


def callback(ch, method, properties, body):
    data = json.loads(body)

    img1 = data['caminho_do_face']
    img2 = data['document_id']
    local = data['nome_equipamento']
    dia= data['data_captura']







@shared_task()
def start_consumer_path():
    logger.info('start_consumer_path')
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port=5672))
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_PUBLISHIR)
        channel.basic_consume(queue=QUEUE_PUBLISHIR, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
    except Exception as e:
        logger.error('start_consumer_path: %s' % e)
        raise self.retry(exc=e)
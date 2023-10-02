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

QUEUE_PUBLISHIR = 'ftp'
EXCHANGE = 'secedu'
ROUTE_KEY = 'path'

FTP_PATH = 'ftp'

# Expressão regular para o padrão AAAA-MM-DD
date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')

@app.task(name='start_consumer_path', bind=True, max_retries=3, default_retry_delay=10)
def start_consumer_path():
    devices = Cameras.objects.all()
    processed_dates = set()  # Para armazenar as datas já processadas

    for root, dirs, files in os.walk(FTP_PATH):
        components = root.split('/')

        # Verificar se o path tem 4 componentes e se corresponde ao padrão AAAA-MM-DD
        if components and len(components) == 4 and date_pattern.match(components[3]):
            date_capture = components[3]

            # Verificar se a data já foi processada
            if date_capture not in processed_dates:
                try:
                    device_name = components[1]
                    timestamp = datetime.now().isoformat()
                    file_path = os.path.join(root)
                    message_dict = {
                        "data_captura": date_capture,
                        "nome_equipamento": device_name,
                        "caminho_do_arquivo": file_path,
                        "data_processamento": timestamp,
                    }

                    message_str = json.dumps(message_dict)
                    logger.info(f'Processing MESSAGE: {message_str}')

                    publisher = Publisher()
                    publisher.start_publisher(exchange=EXCHANGE, routing_name=ROUTE_KEY, message=message_str)
                    publisher.close()

                    # Marcar a data como processada
                    processed_dates.add(date_capture)
                except pika.exceptions.AMQPConnectionError as e:
                    logger.error(f'Error in processing: {e}')

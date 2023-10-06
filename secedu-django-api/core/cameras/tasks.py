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

EXCHANGE = 'secedu'
QUEUE_PUBLISHIR = 'embedding'
ROUTE_KEY = 'verification'

FTP_PATH = 'ftp'

@shared_task()
def start_consumer_path():
    logger.info('start_consumer_path')
    try:
        for root, dirs, files in os.walk(FTP_PATH):
            components = root.split('/')

            # Verificar se o path tem 4 componentes e se corresponde ao padrão AAAA-MM-DD
            if components and len(components) == 4 and date_pattern.match(components[3]):
                date_capture = components[3]

                # Verificar se a data já foi processada
                if date_capture not in processed_dates:
                    logger.info(f' <**_start_consumer_path_**> 2 : {date_capture}')
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
                        logger.info(f' <**_start_consumer_path_**> 3 :  {message_str}')

                        publisher = Publisher()
                        publisher.start_publisher(exchange=EXCHANGE, routing_name=ROUTE_KEY, message=message_str)
                        publisher.close()

                        # Marcar a data como processada
                        processed_dates.add(date_capture)
                    except pika.exceptions.AMQPConnectionError as e:
                        logger.error(f'Error in processing: {e}')
                else:
                    logger.info(f' <**_start_consumer_path_**> 4 : {date_capture} já processada')
                    continue
    except Exception as e:
        logger.error('start_consumer_path: %s' % e)
 
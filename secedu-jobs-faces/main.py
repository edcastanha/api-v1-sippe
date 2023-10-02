from __future__ import absolute_import, unicode_literals
import os
import re
import json
from datetime import datetime
import pika

from loggingMe import logger
from publicar import Publisher

QUEUE_PUBLISHIR = 'ftp'
EXCHANGE = 'secedu'
ROUTE_KEY = 'path'

FTP_PATH = 'ftp'

# Expressão regular para o padrão AAAA-MM-DD
date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')

def start_consumer_path():
    processed_dates = set()  # Para armazenar as datas já processadas
    logger.info(f' <**_start_consumer_path_**> 1 : aguardando fila ...')

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


if __name__ == '__main__':
    start_consumer_path()
import os
import re
import json
from datetime import datetime
import pika
from loggingMe import logger

from publicar import Publisher

logger.info(f' <**_**> Main - Iniciando FTP')

QUEUE_PUBLISHIR='ftp'
#QUEUE_CONSUMER='arquivos'
EXCHANGE='secedu'
ROUTE_KEY='path'
#ASK_DEBUG = False

FTP_PATH = '../volumes/ftp'

# Expressão regular para o padrão AAAA-MM-DD
date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')

# Percorrer a pasta FTP
for root, dirs, files in os.walk(FTP_PATH):
    logger.info(f' <**_**> MAIN Listagem de PATH DEVICE')
    for dir in dirs:
        # Verificar se a subpasta corresponde ao padrão AAAA-MM-DD
        if date_pattern.match(dir):
            try:
                components = root.split('/')
                device_name = components[2]
                date_capture = dir
                timestamp = datetime.now().isoformat()
                file_path = os.path.join(root, dir)
                message_dict = {
                    "data_captura": date_capture,
                    "nome_equipamento": device_name,
                    "caminho_do_arquivo": file_path,
                    "data_processomento": timestamp,
                }
                logger.info(f' <**_**> MAIN : path = {file_path}')

                message_str = json.dumps(message_dict)

                logger.info(f' <**_**> ')
                publisher = Publisher()
                logger.info(f' <**_**> MAIN: {EXCHANGE} - {QUEUE_PUBLISHIR}')
                publisher.start_publisher(exchange=EXCHANGE, routing_name=ROUTE_KEY, message=message_str)
                publisher.close()
            except pika.exceptions.AMQPConnectionError as e:
                logger.error(f' <**_**> MAIN: {e}')
            
    


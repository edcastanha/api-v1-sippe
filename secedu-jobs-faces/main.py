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

# Percorrer a pasta FTP
for root, dirs, files in os.walk(FTP_PATH):
    components = root.split('/')
    #logger.info(f' <**_ 1 _**> MAIN:: {components}')
    # verificar se o path tem 4 componentes
    if components and len(components) == 4:
        #logger.info(f' <**_ 2 _**> MAIN:: {components[3]}')
        # Verificar se a subpasta corresponde ao padrão AAAA-MM-DD
        if date_pattern.match(components[3]):
            try:
                device_name = components[1]
                date_capture = components[3]
                timestamp = datetime.now().isoformat()
                file_path = os.path.join(root)
                message_dict = {
                    "data_captura": date_capture,
                    "nome_equipamento": device_name,
                    "caminho_do_arquivo": file_path,
                    "data_processamento": timestamp,  # Correção no nome da chave
                }

                message_str = json.dumps(message_dict)
                logger.info(f' <**_ 3 _**> MESSAGE:: {message_str}')

                publisher = Publisher()
                #logger.info(f'MAIN: {EXCHANGE} - {QUEUE_PUBLISHIR}')
                publisher.start_publisher(exchange=EXCHANGE, routing_name=ROUTE_KEY, message=message_str)
                publisher.close()
            except pika.exceptions.AMQPConnectionError as e:
                logger.error(f'MAIN: {e}')



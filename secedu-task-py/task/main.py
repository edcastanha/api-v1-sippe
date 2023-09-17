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
FTP_PATH = 'ftp/sippe3/Sippe3/'

date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')

processed_folders = set()  # Conjunto para armazenar as pastas já processadas

def create_message(root, dir):
    timestamp = datetime.now().isoformat()
    file_root = date_pattern.match(dir)  # Corrigido para corresponder ao caminho completo (root)
    if file_root and dir not in processed_folders:  # Verifica se a pasta não foi processada
        logger.info(f' <**_5_**> MAIN: create_message - {file_root}')
        try:
            components = root.split('/')
            device_name = components[2]
            date_capture = dir
            file_path = os.path.join(root, dir)
            message_dict = {
                "data_captura": date_capture,
                "nome_equipamento": device_name,
                "caminho_do_arquivo": file_path,
                "data_processamento": timestamp,
            }
            message_str = json.dumps(message_dict)
            return message_str
        except Exception as e:
            logger.error(f'Exception: {e}')
    else:
        message_dict = {
                "data_processamento": timestamp,
                "processo": "Aguardando Files"
            }
        message_str = json.dumps(message_dict)
    
    return message_str

def main():
    logger.info(f' <**_ 1 _**> {FTP_PATH}')
    for root, dirs, files in os.walk(FTP_PATH):
        for dir in dirs:
            message = create_message(root, dir)
            logger.info(f' <**_ 2 _**> Main - PATH FTP: {root} ')
            if message:
                processed_folders.add(root)  # Adiciona a pasta ao conjunto de pastas processadas
                try:
                    publisher = Publisher()
                    logger.info(f'MAIN: Exchange: {EXCHANGE} - Queue: {QUEUE_PUBLISHIR}')
                    logger.info(f' <**_3_**>  Message = {message}')
                    publisher.start_publisher(exchange=EXCHANGE, routing_name=ROUTE_KEY, message=message)
                    publisher.close()
                except pika.exceptions.AMQPConnectionError as e:
                    logger.error(f'EXCEPTION: {e}')
            else:
                logger.info(f' <**_END_**> Aguardando novas pastas !!!')

if __name__ == "__main__":
    main()

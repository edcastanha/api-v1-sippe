# consumer-rota-cameras-data.py 
# ConsumerPath 
# Extrai PATH de FTP e encaminha Files SNAPSHOT
import pika
import json
from datetime import datetime as dt
import re
import os
from loggingMe import logger

EXCHANGE='secedu'

QUEUE_PUBLISHIR='files'
ROUTE_KEY='snapshot'

QUEUE_CONSUMER='ftp'
ASK_DEBUG = True

from publicar import Publisher

class ConsumerPath:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='localhost',
                port=5672,
                credentials=pika.PlainCredentials('secedu', 'ep4X1!br')
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_bind(
            queue=QUEUE_PUBLISHIR,
            exchange=EXCHANGE,
            routing_key=ROUTE_KEY
        )
        logger.info(f' <**_**> ConsumerPath: init')
    
    def run(self):
        self.channel.basic_consume(
            queue=QUEUE_CONSUMER,
            on_message_callback=self.process_message,
            auto_ack=True
        )
        
        logger.info(f' <**_**> ConsumerPath: aguardando fila ...')
        try:
            self.channel.start_consuming()
            logger.info(f' <**_**> ConsumerPath: start_consuming')
        finally:
            self.connection.close()
            logger.info(f' <**_**> ConsumerPath: close')

    def process_message(self, ch, method, properties, body):
        logger.info(f' <**_**> ConsumerPath: proccess_message')
        data = json.loads(body)
        now = dt.now()
        proccess = now.strftime("%Y-%m-%d %H:%M:%S")
        message_dict = {
            'data_processo': proccess,
            'data_captura': data['data_captura'],
            'nome_equipamento': data['nome_equipamento']
        }

        for index, field_name in data.items():
            logger.info(f' <**_**> ConsumerPath: Corre messagem')
            if index == 'caminho_do_arquivo':
                file_paths = self.find_image_files(field_name)
                publisher = Publisher()
                for file_path in file_paths:
                    message_dict.update({'caminho_do_arquivo': file_path})
                    message_str = json.dumps(message_dict)
                    publisher.start_publisher(exchange=EXCHANGE, routing_name=ROUTE_KEY, message=message_str)
                    logger.info(f' <**_**> ConsumerPath: {file_path}')
                publisher.close()

    def find_image_files(self, path):
        file_paths = []
        for root, directories, files in os.walk(path):
            for file in files:
                if file.lower().endswith(('[0].jpg', '[0].jpeg', '[0].png')):
                    file_path = os.path.join(root, file)
                    file_paths.append(file_path)
        logger.info(f' <**_**> ConsumerPath: find_image_files')
        return file_paths

if __name__ == "__main__":
    job = ConsumerPath()
    job.run()
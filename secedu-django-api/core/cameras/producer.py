import os
import re
import json
from datetime import datetime
import pika

from core.cameras.models import Cameras, Locais, Processamentos
from core.loggingMe import logger
from core.publisher import Publisher
from core.celery import app

EXCHANGE = 'secedu'
ROUTE_KEY = 'path'
QUEUE_PUBLISHIR = 'ftp'

class ProducerCameras:
    def __init__(self):
        self.date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        self.publisher = Publisher()

# Funcao de busca dados no Models do Django Locais e Cameras
    def get_cameras(self):
        locais = Locais.objects.all()
        acessos = []
        for local in locais:
            cameras = Cameras.objects.filter(local=local)
            for camera in cameras:
                acessos.append({
                    'local': local.nome,
                    'equipamento': camera.descricao,
                    'path_ftp': camera.acesso,
                })
        return acessos
    
    def find_image_files(self, path):
        file_paths = []
        for root, directories, files in os.walk(path):
            for file in files:
                if file.lower().endswith(('[0].jpg', '[0].jpeg', '[0].png')):
                    file_path = os.path.join(root, file)
                    file_paths.append(file_path)
        logger.info(f' <**_3_**> ConsumerPath: {file_path}')
        return file_paths

    def process_message(self, ch, method, properties, body):
        logger.info(f' <**_ 2 _**> ConsumerPath: proccess_message')
        data = get_cameras()

        now = dt.now()
        proccess = now.strftime("%Y-%m-%d %H:%M:%S")
        message_dict = {
            'data_processo': proccess,
            'nome_equipamento': data['equipamento']
        }

        for index, field_name in data.items():
            #logger.info(f' <**_**> ConsumerPath: Corre messagem')
            if index == 'path_ftp':
                file_paths = self.find_image_files(field_name)
                for file_path in file_paths:
                    message_dict.update({'caminho_do_arquivo': file_path})
                    message_str = json.dumps(message_dict)
                    self.publisher.start_publisher(exchange=EXCHANGE, routing_name=ROUTE_KEY, message=message_str)
                    logger.info(f' <**_3_**> ConsumerPath: {file_path}')
                self.publisher.close()
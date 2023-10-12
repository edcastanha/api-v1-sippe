import os
import re
import json
from datetime import datetime as dt

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

# Funcao de busca dados no Models do Django Locais e Cameras
    def get_cameras(self):
        cameras = Cameras.objects.all()
        acessos = []
        for camera in cameras:
            locais = Locais.objects.filter(camera=camera.id)
            for local in locais:
                acessos.append({
                    'local': local.nome,
                    'camera': camera.descricao,
                    'path': camera.acesso,
                })
        return acessos
    
    def find_image_files(self, path):
        file_paths = []
        for root, directories, files in os.walk(path):
            for file in files:
                if file.lower().endswith(('[0].jpg', '[0].jpeg', '[0].png')):
                    file_path = os.path.join(root, file)
                    file_paths.append(file_path)
        
        logger.info(f'<**_ProducerCameras_**> Find_Image_Files:: {file_paths}')
        
        return file_paths

    def process_message(self, message_dict):
        publisher = Publisher()
        
        message_str = json.dumps(message_dict)
        publisher.publish_message(
            exchange=EXCHANGE,
            routing_key=ROUTE_KEY,
            queue=QUEUE_PUBLISHIR,
            message=message_str
        )
        publisher.close()
        logger.info(f'<**_ProducerCameras_**> proccess_message:: {message_str}')

    def start_run(self):
        logger.info(f' <**_ProcedurCameras_**> Start RUN : 1 ...')
        cameras = self.get_cameras()

        #{
        #  'local': local.nome,
        #  'camera': camera.descricao,
        #  'path': camera.acesso,
        #}
        for obj in cameras:
            processed_dates = set() # Para armazenar as datas já processadas
            message_dict = {
            'local': obj['local'],
            'camera': obj['camera']
            }
            
            for root, dirs, files in os.walk(obj['path']):
                components = root.split('/')

            # Verificar se o path tem 4 componentes e se corresponde ao padrão AAAA-MM-DD
                if components and len(components) == 4 and date_pattern.match(components[3]):
                    data_processadas = Processamentos.objects.filter(camera=obj['camera'])
                    
                    date_capture = components[3]

                    # Verificar se a data já foi processada
                    if date_capture not in data_processadas['data_captura'] and date_capture not in processed_dates:
                        logger.info(f' <**_start_consumer_path_**> 2 : {date_capture}')
                        message_dict.update({"data_captura": date_capture})
                        try:
                            message_str = json.dumps(message_dict)
                            logger.info(f' <**_start_consumer_path_**> 3 :  {message_str}')

                            publisher = Publisher()
                            publisher.start_publisher(exchange=EXCHANGE, routing_name=ROUTE_KEY, message=message_str)
                            publisher.close()

                            # Marcar a data como processada
                            processed_dates.add(date_capture)
                        except publisher.exceptions.AMQPConnectionError as e:
                            logger.error(f'Error in processing: {e}')
                    else:
                        logger.info(f' <**_start_consumer_path_**> 4 : {date_capture} já processada')
                        continue

        for obj in objs:
            message_dict = {
            'local': obj['local'],
            'camera': obj['camera']
            }
            logger.debug(f' <**_ProducerCameras_**>message:: {message_dict}')
            path = obj['path']
            file_paths = self.find_image_files(path)
            for file_path in file_paths:
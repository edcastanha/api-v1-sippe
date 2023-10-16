import os
import re
import json
from datetime import datetime as dt

from core.cameras.models import Cameras, Locais, Processamentos
from core.loggingMe import logger
from core.publisher import Publisher
from core.celery import app

class ProducerCameras:
    def __init__(self):
        logger.debug(f' <**_ProducerCameras_**> INIT : {self}')
        self.exchanges = 'secedu'
        self.routing_key = 'path'
        self.queue = 'ftp'
    

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
    
    def find_image_files(self, path, messege_base):
        for root, directories, files in os.walk(path):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    file_path = os.path.join(root, file)
                    self.process_message(file_path)
                    logger.info(f'<**_ProducerCameras_**> 6 Find_Image_Files:: {file_path}')
        
    
    def is_valid_date_path(self, path):
        # Padrão regex para AAAA-MM-DD
        date_pattern = r'\d{4}-\d{2}-\d{2}'
        
        # Verifica se o caminho contém o padrão AAAA-MM-DD em algum lugar
        if re.search(date_pattern, path):
            logger.debug(f' <**_ProducerCameras_**> 4 : PATH => {path}')
            return True
        else:
            logger.debug(f' <**_ProducerCameras_**> 4 : PATH  => {path}')
            return False
            
    def process_message(self, message_dict):
        publisher = Publisher()
        message_str = json.dumps(message_dict)
        publisher.start_publisher(
            exchange=self.exchanges,
            routing_name=self.routing_key,
            message=message_str
        )
        publisher.close()
        logger.info(f'<**_ProducerCameras_**> proccess_message:: {message_str}')

    def start_run(self):
        logger.debug(f' <**_ProcedurCameras_**> Start RUN ...')
        
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
            logger.debug(f' <**_ProcedurCameras_**> 1 : {obj}')

            root_path = f'media/{obj["path"]}'
            if os.path.exists(root_path):
                logger.debug(f' <**_ProcedurCameras_**> 2 : ROOT PATH=> {root_path}')
                for root, dirs, files in os.walk(root_path):                
                    logger.debug(f' <**_ProcedurCameras_**> 3 : ROOT => {root}')
                    logger.debug(f' <**_ProcedurCameras_**> 3.1 : DIRS => {dirs}')
                    
                    path_files = f'{root}{dirs[-1]}'
                    if self.is_valid_date_path(path_files):
                        logger.debug(f' <**_ProcedurCameras_**> 4.1 : DIA => {dir}')
                        for dir in dirs:
                            procemento = Processamentos.objects.filter(camera=obj, dia=dir).exists()
                            logger.debug(f' <**_ProcedurCameras_**> 5 : PROCESSAMENTOS => {procemento}')
                            if dir not in processed_dates:
                                logger.debug(f' <**_ProcedurCameras_**> 6 : FiLE=> {root}/{dir}')
                                processed_dates.add(dir)
                                message_dict['date'] = dir
                                self.find_image_files(path=f'{root}{dir}', messege_base=message_dict)
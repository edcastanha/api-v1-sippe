import os
import re
import json
from datetime import datetime as dt
from django.core.exceptions import ObjectDoesNotExist

from core.cameras.models import Cameras, Locais, Processamentos
from core.loggingMe import logger
from core.publisher import Publisher

class ProducerCameras:
    def __init__(self):
        self.exchanges = 'secedu'
        self.routing_key = 'path'
        self.queue = 'ftp'
        self.local = None
        self.device = None
        self.capture_date = None
        self.capture_hour = None

    def get_cameras(self):
        cameras = Cameras.objects.all()
        acessos = []
        for camera in cameras:
            locais = Locais.objects.filter(camera=camera)
            for local in locais:
                acessos.append({
                    'local': local.nome,
                    'camera': camera.id,
                    'path': camera.acesso,
                })
        return acessos
    
    def get_prossessamentos(self):
        processamentos = Processamentos.objects.filter(status='Inicializado').order_by('id')
        #processamentos = Processamentos.objects.exclude(status='Processado').order_by('id')
        logger.debug(f'<**_ProducerCameras_**> 10 Get_Prossessamentos :: {processamentos}')
        acessos = []
        for processamento in processamentos:
            acessos.append({
                'data_processo': dt.now().strftime("%Y-%m-%d %H:%M:%S"),
                'data_captura': processamento.dia,
                'nome_equipamento': processamento.camera.id,
                'local': '',
                'path_file': processamento.path,
                'status': processamento.status,
                'horario': processamento.horario,
                'proccess_id': processamento.id
            })
            
        return acessos

    def find_image_files(self, path):
        message_dict = {
            'data_processo': dt.now().strftime("%Y-%m-%d %H:%M:%S"),
            'data_captura': self.capture_date,
            'nome_equipamento': self.device,
            'local': self.local,
        }
        logger.debug(f'<**_ProducerCameras_**> 5 Find_Image_Files :: PATH {path}')
        
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    file_path = os.path.join(root, file)
                    self.capture_hour = self.is_valid_hour_path(file_path)
                    if not Processamentos.objects.filter(path=file_path).exists() and self.capture_hour is not None:
                        message_dict.update({'path_file': file_path})
                        message_dict.update({'horario': self.capture_hour})
                        logger.debug(f'<**_ProducerCameras_**> 6 Find_Image_Files MSG_DICT :: {message_dict}')
                        self.create_processamento(message_dict, file_path)
     
    def is_valid_hour_path(self, file):       
       # Tente encontrar o padrão HH:MM:SS ou HH:MM.SS no caminho do arquivo
        match = re.search(r'/(\d{2})/(\d{2})/(\d{2})|/(\d{2})/(\d{2})\.(\d{2})', file)
        
        if match:
            groups = match.groups()
            if groups[0] is not None:
                hh, mm, ss = groups[0:3]
                #logger.debug(f'<**_**> is_valid_hour_path: Match 1 - HH/MM/SS')
            else:
                hh, mm, ss = groups[3:6]
                #logger.debug(f'<**_**> is_valid_hour_path: Match 2 - HH/MM.SS')
        return f'{hh}h{mm}m{ss}s'

    def is_valid_date_path(self, path):
        # Padrão regex para AAAA-MM-DD
        date_pattern = r'\d{4}-\d{2}-\d{2}'
        #logger.debug(f'<**_ProducerCameras_**> is_valid_date_path:: {path}')
        
        # Verifica se o caminho contém o padrão AAAA-MM-DD em algum lugar
        return re.search(date_pattern, path) is not None

    def create_processamento(self, message_dict, file_path):
        camera = Cameras.objects.get(id=self.device)  # Obtenha a instância da câmera
        logger.debug(f'<**_ProducerCameras_**> 7 Create_Processamento Devide :: {camera}')
        try:
            new_registro = Processamentos.objects.create(
                camera=camera,  # Use a instância da câmera, não o ID
                dia=self.capture_date,
                horario=self.capture_hour,
                path=file_path
            )
            message_dict.update({'proccess_id': new_registro.id})
            logger.debug(f'<**_ProducerCameras_**> 8 Create_Processamento :: {new_registro.id}')
            
            message_str = json.dumps(message_dict)
            logger.debug(f'<**_ProducerCameras_**> 9 Publisher :: {message_str}')
            self.process_message(message_str)
        except ObjectDoesNotExist as e:
            logger.error(f'Câmera não encontrada: {e}')
        except ValueError as e:
            logger.error(f'Erro ao criar o objeto Processamentos: {e}')
            
        
    def process_message(self, message):
        publisher = Publisher()
        try:
            publisher.start_publisher(
                exchange=self.exchanges,
                routing_name=self.routing_key,
                message=message
            )
            #logger.debug(f'<**_ProducerCameras_**> 4 proccess_message:: {message}')
        finally:
            publisher.close()
            #logger.debug(f'<**_ProducerCameras_**> 5 CLOSE PUBLISHER:: {message}')

    def start_run(self):
        logger.debug(f'<**_ProcedurCameras_**> Start Producer Cameras -- Capturas por Dia ...')
        registros = self.get_prossessamentos()
        if len(registros) > 0:
            for registro in registros:
                message_retry = json.dumps(registro)
                logger.debug(f'<**_ProcedurCameras_**> 0 Message Retry : {message_retry}')
                self.process_message(message=message_retry)
    
        cameras = self.get_cameras()
        logger.debug(f'<**_ProcedurCameras_**> 0 CAMERAS : {cameras}')
        if len(cameras) > 0:
            for obj in cameras:
                self.device = obj['camera']
                self.local = obj['local']

                logger.debug(f'<**_ProcedurCameras_**> 1 : {obj}')

                root_path = f'media/{obj["path"]}'
                if os.path.exists(root_path):
                    logger.debug(f'<**_ProcedurCameras_**> 2 : ROOT PATH=> {root_path}')
                    
                    for root, dirs, files in os.walk(root_path):
                        for dir in dirs:
                            logger.debug(f'<**_ProcedurCameras_**> 3 : DIR=> {dir}')
                            path_data = os.path.join(root_path, dir)
                            #logger.debug(f'<**_ProcedurCameras_**> 3.1 : PATH DATA=> {path_data}')
                            if self.is_valid_date_path(path_data):
                                self.capture_date = dir
                                logger.debug(f'<**_ProcedurCameras_**> 4 : Captura Date=> {self.capture_date}')
                                self.find_image_files(path=path_data)

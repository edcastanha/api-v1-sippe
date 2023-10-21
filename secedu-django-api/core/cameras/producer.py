import os
import re
import json
from datetime import datetime as dt
from django.core.exceptions import ObjectDoesNotExist

from core.cameras.models import Cameras, Locais, Processamentos
from core.loggingMe import logger
from core.publisher import Publisher

class ProducerCameras:
    """
    Class that handles the production of messages related to cameras and their processing.

    Attributes:
        exchanges (str): The name of the exchange to be used for publishing messages.
        routing_key (str): The routing key to be used for publishing messages.
        queue (str): The name of the queue to be used for publishing messages.
        local (str): The name of the location where the camera is installed.
        device (str): The ID of the camera device.
        capture_date (str): The date when the image was captured.
        capture_hour (str): The time when the image was captured.
    """

    def __init__(self):
        self.exchanges = 'secedu'
        self.routing_key = 'path'
        self.queue = 'ftp'
        self.local = None
        self.device = None
        self.capture_date = None
        self.capture_hour = None
        self.processamento_path = None
        self.processamento_exists = None
        self.task_date = dt.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_cameras(self):
        """
        Retrieve all cameras and their associated locations from the database.

        Returns:
            list: A list of dictionaries containing the location, camera ID and access path for each camera.
        """
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
    
    def find_image_files(self, path):
        """
        Find all image files in the specified path and create a processamento object for each new file.

        Args:
            path (str): The path to search for image files.
        """
        message_dict = {
            'data_processo': self.task_date,
            'data_captura': self.capture_date,
            'nome_equipamento': self.device,
            'local': self.local,
        }
        
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    self.processamento_path = str(os.path.join(root, file))
                    self.capture_hour = self.is_valid_hour_path()
                    try:
                        self.processamento_exists = Processamentos.objects.get(path=self.processamento_path)
                        # Finalizar a task Celery com success
                        logger.info('<**_ProducerCameras_**>PATH EXIST :: %s | PATH ::  %s', self.processamento_exists, self.processamento_path)
                    except Processamentos.DoesNotExist:
                        self.processamento_exists = False
                        message_dict.update({'path_file': self.processamento_path})
                        message_dict.update({'horario': self.capture_hour})
                        logger.info('<**_ProducerCameras_**> PATH  EXIST::%s | PATH :: %s', self.processamento_exists, self.processamento_path)
                        self.create_processamento(message_dict)                       
                    except Exception as e:
                        logger.error('<**_ProducerCameras_**> Error: %s ', e)
    
    def is_valid_hour_path(self):       
        """
        Check if the file path contains a valid time stamp.

        Args:
            file (str): The file path to check.

        Returns:
            str: The time stamp in the format 'HHhMMmSSs'.
        """
        # Tente encontrar o padrão HH:MM:SS ou HH:MM.SS no caminho do arquivo
        match = re.search(r'/(\d{2})/(\d{2})/(\d{2})|/(\d{2})/(\d{2})\.(\d{2})', self.processamento_path)
        if match:
            groups = match.groups()
            if groups[0] is not None:
                hh, mm, ss = groups[0:3]
            else:
                hh, mm, ss = groups[3:6]
        return f'{hh}h{mm}m{ss}s'

    def is_valid_date_path(self, path):
        """
        Check if the file path contains a valid date.

        Args:
            path (str): The file path to check.

        Returns:
            bool: True if the path contains a valid date, False otherwise.
        """
        # Padrão regex para AAAA-MM-DD
        date_pattern = r'\d{4}-\d{2}-\d{2}'
        #logger.info(f'<**_ProducerCameras_**> is_valid_date_path:: {path}')
        
        # Verifica se o caminho contém o padrão AAAA-MM-DD em algum lugar
        return re.search(date_pattern, path) is not None

    def create_processamento(self, message_dict):
        """
        Create a new Processamento object and publish a message with its data.

        Args:
            message_dict (dict): A dictionary containing the data to be published.
        """
        try:
            camera = Cameras.objects.get(id=self.device)
            new_registro = Processamentos.objects.create(
                camera=camera,  # Use the camera instance, not the ID
                dia=self.capture_date,
                horario=self.capture_hour,
                path=self.processamento_path
            )
            message_dict.update({'proccess_id': new_registro.id})
            logger.info('<**_ProducerCameras_**> 6 Create_Processamento :: %s', new_registro.id)
            
            message_str = json.dumps(message_dict)
            logger.info('<**_ProducerCameras_**> 7 Publisher :: %s', message_str)
            self.process_message(message_str)
        except ObjectDoesNotExist as e:
            logger.debug('Error object: %s', e)    
        except ValueError as e:
            logger.debug('Error creating Processamentos object: %s', e)
        
    def process_message(self, message):
        """
        Publish a message to the RabbitMQ exchange.

        Args:
            message (str): The message to be published.
        """
        publisher = Publisher()
        try:
            publisher.start_publisher(
                exchange=self.exchanges,
                routing_name=self.routing_key,
                message=message
            )
            logger.info('<**_ProducerCameras_**> 8 process_message :: %s', message)
        finally:
            publisher.close()
            logger.info('<**_ProducerCameras_**> 9 CLOSE PUBLISHER :: %s', message)

    def start_run(self):
        cameras = self.get_cameras()
        logger.info(f'<**_ProcedurCameras_**> START PRODUCER : {self.task_date}')
        if len(cameras) > 0:
            for obj in cameras:
                self.device = obj['camera']
                self.local = obj['local']
                root_path = f'media/{obj["path"]}'
                if os.path.exists(root_path):                    
                    for root, dirs, files in os.walk(root_path):
                        for dir in dirs:
                            path_data = os.path.join(root_path, dir)
                            if self.is_valid_date_path(path_data):
                                self.capture_date = dir
                                try:
                                    self.find_image_files(path=path_data)
                                except Exception as e:
                                    logger.error(f'<**_ProducerCameras_**> Error processing path: {e}')
            
            logger.info('<**_ProducerCameras_**> END PRODUCER | date: %s - file exist: %s | %s',self.task_date, self.processamento_exists, self.processamento_path)
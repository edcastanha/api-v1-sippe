import pika
import json
from datetime import datetime as dt
import os
#import re
import numpy as np
import uuid
import cv2
import mediapipe as mp

#import redis
#from redis.commands.search.field import VectorField, TagField
#from redis.commands.search.query import Query

from deepface import DeepFace
from publicar import Publisher
from loggingMe import logger

REDIS_SERVER = 'redis-server'
RMQ_SERVER = 'broker-server'

EXCHANGE='secedu'
QUEUE_PUBLISHIR='faces'
ROUTE_KEY='extrair'

QUEUE_CONSUMER='ftp'
ASK_DEBUG = True

#BACKEND_DETECTOR='retinaface'
#MODEL_BACKEND ='Facenet'
#LIMITE_DETECTOR = 0.996

BACKEND_DETECTOR='retinaface'
MODEL_BACKEND ='Facenet'
DISTANCE_METRIC = 'euclidean'
LIMITE_DETECTOR = 0.9740

DIR_CAPTURE = '/app/media/capturas/'

#r = redis.StrictRedis(host=REDIS_SERVER, port=6379, db=0)

# celery -A core worker producer task path
class ConsumerExtractor:
    def __init__(self):
        self.path_capture = DIR_CAPTURE
        self.backend_detector = BACKEND_DETECTOR
        self.model_backend = MODEL_BACKEND
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RMQ_SERVER,
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

        #logger.debug(f' <**_ 1 _**> RMQ_SERVER::{RMQ_SERVER} REDIS_SERVER::{REDIS_SERVER} PATH:: {self.path_capture}')

    def run(self):
        logger.debug(f' <**_0_**> ConsumerExtractor: RUN')
        self.channel.basic_consume(
            queue=QUEUE_CONSUMER,
            on_message_callback=self.process_message,
            auto_ack=ASK_DEBUG
        )

        try:
            self.channel.start_consuming()
        finally:
            self.connection.close()
            logger.debug(f' <**_**> ConsumerExtractor: close')

    def process_message(self, ch, method, properties, body):
        data = json.loads(body)
        file = data['path_file']
        horario = data['horario']
        device = data['local']
        logger.debug(f' <**_1_**> ConsumerExtractor: process_message:: {data}')

        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            now = dt.now()
            equipamento =data['nome_equipamento']
            data_captura=data['data_captura']
            processamento = now.strftime("%Y-%m-%d %H:%M:%S")
            message_dict = {
                'data_processo': processamento,
                'data_captura': data_captura,
                'hora_captura': horario,
                'nome_equipamento': equipamento,
                'local_equipamento': device,
                'captura_base': file,
            }
            logger.debug(f' <**_2_**> ConsumerExtractor:  process_message:: {message_dict}')
            
            publisher = Publisher()
            face_objs = DeepFace.extract_faces(
                                        img_path=file,
                                        detector_backend=self.backend_detector,
                                        enforce_detection=False,
                                        
                                        align=True
                                    )

            try:
                logger.debug(f' <**_3_**> ConsumerExtractor:  TRY face_objs:: {face_objs}')
                for index, face_obj in enumerate(face_objs):
                    if face_obj['confidence'] >= LIMITE_DETECTOR:
                        face = face_obj['face']
                        new_face = os.path.join(str(self.path_capture), str(equipamento), str(data_captura), str(horario))
                        logger.debug(f' <**_4_**> ConsumerExtractor: face_path :: {new_face}')

                        if not os.path.exists(new_face):
                            os.makedirs(new_face, exist_ok=True)

                        # Converta a imagem de float32 para uint8 (formato de imagem)
                        face_uint8 = (face * 255).astype('uint8')
                        
                        # Gere um nome de arquivo único para a face
                        save_path = os.path.join(new_face, f"face_{index}.jpg")
                        logger.debug(f' <**_5_**> SAVE NEW FACE Path:: {save_path}: ')
                        
                        
                        # Salve a face no diretório "captura/" usando OpenCV
                        cv2.imwrite(save_path, cv2.cvtColor(face_uint8, cv2.COLOR_RGB2BGR))
                        message_dict.update({'caminho_do_face': save_path})
                        message_dict.update({'detector_backend': self.backend_detector})
                        message_str = json.dumps(message_dict)
                        publisher.start_publisher(exchange=EXCHANGE, routing_name=ROUTE_KEY, message=message_str)
                        logger.debug(f' <**_6_**> ConsumerExtractor:  message_str:: {message_str}')
                publisher.close()
            except Exception as e:
                logger.debug(f' <**_3_**> TRY Erro:: {e}')
    
if __name__ == "__main__":
    job = ConsumerExtractor()
    job.run()
import pika
import json
from datetime import datetime as dt
from lib.deepface import DeepFace

import redis
from redis.commands.search.field import VectorField, TagField
from redis.commands.search.query import Query

import matplotlib.pyplot as plt

from publicar import Publisher
from loggingMe import logger

EXCHANGE='secedu'

QUEUE_PUBLISHIR='embedding'
ROUTE_KEY='verification'

QUEUE_CONSUMER='faces'
ASK_DEBUG = True

DIR_CAPS ='../volumes/capturas'
BACKEND_DETECTOR='Facenet'
MODEL_BACKEND ='mtcnn'
LIMITE_DETECTOR =0.99

METRICS = ["cosine", "euclidean", "euclidean_l2"]

redis = redis.StrictRedis(host='localhost', port=6379, db=0)


class ConsumerEmbbeding:
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
        logger.info(f' <**_**> ConsumerEmbbeding: Init')

    def run(self):
        # CONFIGURACAO CONSUMER
        self.channel.basic_consume(           
            queue=QUEUE_CONSUMER,
            on_message_callback=self.process_message,
            auto_ack=ASK_DEBUG
        )

        logger.info(f' <**_**> ConsumerEmbbeding: Aguardando {QUEUE_CONSUMER}')
        try:
            self.channel.start_consuming()
            logger.info(f' <**_**> ConsumerEmbbeding: start_consumer')
        finally:
            self.connection.close()
            logger.info(f' <**_**> ConsumerEmbbeding: close')

    def process_message(self, ch, method, properties, body):
        data = json.loads(body)
        file = data['caminho_do_face']
        logger.info(f' <**_**> ConsumerEmbbeding: process_message')

        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            now = dt.now()
            equipamento =data['nome_equipamento']
            data_captura=data['data_captura']
            face=data['caminho_do_face']
            proccess = now.strftime("%Y-%m-%d %H:%M:%S")
            message_dict = {
                'nome_equipamento': equipamento,
                'data_captura': data_captura,
                'caminho_do_face': face,
                'data_processo': proccess,

            }

            try:
   
                embedding = DeepFace.represent(img_path=face,
                                               detector_backend=BACKEND_DETECTOR, 
                                               enforce_detection=False,
                                               detector_backend=MODEL_BACKEND
                                               )[0]["embedding"]
                message_dict.update({'embedding': embedding})

                publisher = Publisher()
                message_dict.update({'detector_backend': BACKEND_DETECTOR})
                message_str = json.dumps(message_dict)
                publisher.start_publisher(exchange=EXCHANGE, routing_name=ROUTE_KEY, message=message_str)
                publisher.close()
                logger.info(f' <**_**>  ConsumerEmbbeding: Embedding ')
            except Exception as e:
                logger.error(f' <**_**> ConsumerEmbbeding: Salve e Publisher ')

if __name__ == "__main__":
    job = ConsumerEmbbeding()
    job.run()
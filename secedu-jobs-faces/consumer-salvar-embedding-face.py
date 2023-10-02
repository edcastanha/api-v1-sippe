import pika
import json
from datetime import datetime as dt
from deepface import DeepFace
import numpy as np

import redis
from redis.commands.search.field import VectorField, TagField
from redis.commands.search.query import Query

r = redis.StrictRedis(host='secedu-rds-tack', port=6379, db=0)

import matplotlib.pyplot as plt

from publicar import Publisher
from loggingMe import logger


RMQ_SERVER = 'secedu-rmq-task'
EXCHANGE='secedu'

QUEUE_PUBLISHIR='embedding'

ROUTE_KEY='verification'
QUEUE_CONSUMER='faces'
ASK_DEBUG = True

DIR_CAPS ='capturas'
DIR_DATASET ='dataset'
BACKEND_DETECTOR='Facenet'
MODEL_BACKEND ='mtcnn'
LIMITE_DETECTOR =0.99
PESO = 10

METRICS = 'euclidean'



class ConsumerEmbbeding:
    def __init__(self):
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
        logger.info(f' <**ConsumerEmbbeding**> : Init')

    def run(self):
        # CONFIGURACAO CONSUMER
        self.channel.basic_consume(           
            queue=QUEUE_CONSUMER,
            on_message_callback=self.process_message,
            auto_ack=ASK_DEBUG
        )

        try:
            logger.info(f' <**_start consumer_**> FILA:: {QUEUE_CONSUMER}')
            self.channel.start_consuming()
        finally:
            self.connection.close()
            logger.info(f' <**_**> ConsumerEmbbeding: close')

    def process_message(self, ch, method, properties, body):
        data = json.loads(body)
        file = data['caminho_do_face']
        logger.info(f' <**_Proccess_**> {file}')

        if file.endswith(('.jpg', '.jpeg', '.png')):
            message_dict = {
                'nome_equipamento':data['nome_equipamento'],
                'data_captura': data['data_captura'],
                'caminho_do_face': file,
                'detector_backend': BACKEND_DETECTOR,
            }
            #logger.info(f' <**FILE**> {message_dict}')

            try:
                target_embedding = DeepFace.represent(
                    img_path=file,
                    model_name=BACKEND_DETECTOR,
                    detector_backend=MODEL_BACKEND,
                    enforce_detection=False,
                    )[0]["embedding"]

                query_vector = np.array(target_embedding).astype(np.float32).tobytes()
                #logger.info(f' <**_DeepFace_**> Query Vetor:: {query_vector}')

                k = 2
                base_query = f"*=>[KNN {k} @embedding $query_vector AS distance]"
                query = Query(base_query).return_fields("distance").sort_by("distance").dialect(2)
                results = r.ft().search(query, query_params={"query_vector": query_vector})
                #logger.info(f' <**REDIS**> Search:: {results}')

                publisher = Publisher()
                for document in results.docs:
                    document_id = document["id"]
                    distance_str = document["distance"]

                    distance = float(distance_str)
                    
                    if distance <= 10:
                        verify = DeepFace.verify(
                            img1_path=file,
                            img2_path=document_id,
                            model_name=BACKEND_DETECTOR,
                            detector_backend=MODEL_BACKEND,
                            enforce_detection=False,
                            distance_metric=METRICS
                        )
                        logger.info(f' <**_DeepFace_**> Verify:: {verify}')
                        message_dict.update({'document_id': document_id})
                        message_dict.update({'distance' : distance})
                        message_str = json.dumps(message_dict)
                        publisher.start_publisher(exchange=EXCHANGE, routing_name=ROUTE_KEY, message=message_str)
                        logger.info(f' <**_PUBLISHER_**> Messagem:: {message_str} ')
                publisher.close()
            except Exception as e:
                logger.error(f'<**FALHA**> Error:: {str(e)}')

if __name__ == "__main__":
    job = ConsumerEmbbeding()
    job.run()
import pika
import json
from datetime import datetime as dt
from deepface import DeepFace
import numpy as np
import redis
from redis.commands.search.field import VectorField, TagField
from redis.commands.search.query import Query
import matplotlib.pyplot as plt
from publicar import Publisher
from loggingMe import logger
from conectionDB import DatabaseConnection    

class Configuration:
    RMQ_SERVER = 'broker-server'
    RMQ_PORT = 5672
    RMQ_USER = 'secedu'
    RMQ_PASS = 'ep4X1!br'
    RMQ_EXCHANGE = 'secedu'
    RMQ_QUEUE_PUBLISHIR = 'embedding'
    RMQ_QUEUE_CONSUMER = 'faces'
    RMQ_ROUTE_KEY = 'verify'
    RMQ_ASK_DEBUG = True

    REDIS_SERVER = 'redis-server'
    REDIS_PORT = 6379
    REDIS_DB = 0
    REDIS_SSL = False

    BACKEND_DETECTOR = 'retinaface'
    MODEL_BACKEND = 'Facenet'
    DISTANCE_METRIC = 'euclidean_l2'
    LIMITE_DETECTOR = 0.96
    LIMITE_AREA = 80
    ENFORCE_DETECTION = False

    DIR_CAPS ='/app/media/capturas'
    DIR_DATASET ='/app/media/dataset'

    UPDATE_QUERY = """
        UPDATE 
            cameras_processamentos 
        SET 
            status = %s WHERE id = %s
    """

    INSER_QUERY = """
        INSERT INTO cameras_faces 
            (data_cadastro, data_atualizacao, processamento_id, path_face, backend_detector, model_detector, distance_metric, auditado)
        VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s)
    """

class ConsumerEmbbeding:
    def __init__(self):
        self.peso = self.findThreshold(Configuration.MODEL_BACKEND)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host = Configuration.RMQ_SERVER,
                port = Configuration.RMQ_PORT,
                credentials=pika.PlainCredentials(
                    Configuration.RMQ_USER, 
                    Configuration.RMQ_PASS
                )
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_bind(
            queue = Configuration.RMQ_QUEUE_PUBLISHIR,
            exchange = Configuration.RMQ_EXCHANGE,
            routing_key = Configuration.RMQ_ROUTE_KEY
        )
        self.redis_client = redis.Redis(
            host = Configuration.REDIS_SERVER, 
            port = Configuration.REDIS_PORT, 
            db = Configuration.REDIS_DB, 
            ssl = Configuration.REDIS_SSL
        )

    def run(self):
        logger.info(f' <**ConsumerEmbbeding**> : Init ')
        self.channel.basic_consume(           
            queue = Configuration.RMQ_QUEUE_CONSUMER,
            on_message_callback = self.process_message,
            auto_ack = Configuration.RMQ_ASK_DEBUG
        )

        try:
            logger.info(f' <**_start consumer_**> FILA:: {Configuration.RMQ_QUEUE_CONSUMER}')
            self.channel.start_consuming()
        finally:
            self.connection.close()
            logger.info(f' <**_**> ConsumerEmbbeding: close')

    def findThreshold(self, model_name):
        threshold = 0
        #dims = 128
        if model_name == 'VGG-Face':
            threshold = 0.55
            #dims = 2622
        elif model_name == 'OpenFace':
            threshold = 0.55
        elif model_name == 'Facenet':
            threshold = 10
        elif model_name == 'DeepFace':
            threshold = 64

        return threshold

    def process_message(self, ch, method, properties, body):
        data = json.loads(body)
        file = str(data['caminho_do_face'])
        if data['detector_backend'] != None and data['detector_backend'] != '':
            self.detector_backend = str(data['detector_backend'])
        
        if file.endswith(('.jpg', '.jpeg', '.png')):
            try:

                message_dict = {
                    'caminho_do_face': file,
                    'detector_backend': Configuration.BACKEND_DETECTOR,
                    'model_name': Configuration.MODEL_BACKEND,
                    'metrics': Configuration.DISTANCE_METRIC,
                }

                # Exemplo de consulta de atualização
                id_procesamento = data['proccess_id']
                update_query = """
                    UPDATE cameras_processamentos
                    SET status = %s
                    WHERE id = %s
                """

                target_embedding = DeepFace.represent(
                    img_path = file,
                    model_name = Configuration.MODEL_BACKEND,
                    detector_backend = Configuration.BACKEND_DETECTOR,
                    enforce_detection = Configuration.ENFORCE_DETECTION,
                )[0]["embedding"]

                query_vector = np.array(target_embedding).astype(np.float32).tobytes()

                k = 2
                base_query = f"*=>[KNN {k} @embedding $query_vector AS distance]"
                query = Query(base_query).return_fields("distance").sort_by("distance").dialect(2)
                results = self.redis_client.ft().search(query, query_params={"query_vector": query_vector})
                
                publisher = Publisher()
                for idx, result in enumerate(results.docs):
                    logger.info(f"O vizinho mais próximo é {result.id} com distância {result.distance}")

                    dataset_file = str(result.id)
                    
                    message_dict.update({'id_equipamento':data['nome_equipamento']})
                    message_dict.update({'data_captura': data['data_captura']})
                    message_dict.update({'hora_captura': data['hora_captura']})
                    message_dict.update({'captura_base': data['captura_base']})



                    distance = float(result.distance)
                    if distance <= self.peso:
                        verify = DeepFace.verify(
                            img1_path = file,
                            img2_path = dataset_file,
                            model_name = Configuration.MODEL_BACKEND,
                            detector_backend = Configuration.BACKEND_DETECTOR,
                            distance_metric = Configuration.DISTANCE_METRIC,
                            enforce_detection = Configuration.ENFORCE_DETECTION,
                        )

                        logger.info(f' <*_ConsumerEmbbeding_*>DeepFace:: {verify} VERIFY')
                        message_dict.update({'file_dataset': dataset_file})
                        message_dict.update({'distance' : distance})

                        message_str = json.dumps(message_dict)
                        publisher.start_publisher(exchange = Configuration.RMQ_EXCHANGE, 
                                                  routing_name = Configuration.RMQ_ROUTE_KEY, 
                                                  message = message_str
                                                  )
                        db_connection.update(update_query, ('Processado', id_procesamento))

                publisher.close()
                db_connection.close()

            except Exception as e:
                logger.error(f'<**ConsumerEmbbeding**> process_message :: {str(e)}')

if __name__ == "__main__":
    job = ConsumerEmbbeding()
    job.run()
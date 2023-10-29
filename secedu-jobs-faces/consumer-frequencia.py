import pika
import re
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
from configuration import Configuration as config

class Configuration(config):
    
    RMQ_QUEUE_CONSUMER = 'embedding'
    RMQ_ASK_DEBUG = False

    BACKEND_DETECTOR = 'retinaface'
    MODEL_BACKEND = 'Ensemble'
    DISTANCE_METRIC = 'euclidean_l2'
    LIMITE_DETECTOR = 0.96
    LIMITE_AREA = 80
    ENFORCE_DETECTION = False

    UPDATE_QUERY = """
        UPDATE 
            cameras_processamentos 
        SET 
            status = %s WHERE id = %s
    """

    INSER_QUERY = """
        INSERT INTO cameras_face
            (data_cadastro, data_atualizacao, processamento_id, path_face, backend_detector, model_detector, distance_metric, auditado)
        VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s)
    """

class ConsumerFrequency:
    def __init__(self):
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
        self.publisher = Publisher()
        self.db_connection = DatabaseConnection()

    def run(self):
        logger.info(f' <**ConsumerEmbbeding**> : Init ')
        self.channel.basic_consume(           
            queue = Configuration.RMQ_QUEUE_CONSUMER,
            on_message_callback = self.process_message,
            auto_ack = Configuration.RMQ_ASK_DEBUG
        )

        try:
            self.channel.start_consuming()
        finally:
            logger.info(f' <**_**> ConsumerEmbbeding: close')
            if self.connection.is_open:
                self.connection.close()
            if self.db_connection.is_connected():
                self.db_connection.close()
            if self.publisher.connection.is_open:
                self.publisher.close()
            if self.redis_client.connection_pool:
                try:
                    self.redis_client.connection_pool.disconnect()
                    self.redis_client.close()
                except Exception as e:
                    # Handle the exception
                    print(f"An error occurred: {e}")


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

                for idx, result in enumerate(results.docs):
                    logger.info(f"Index:: {idx+1} mais próximo {result.id} com distância {result.distance}")

                    dataset_file = str(result.id)
                    
                    message_dict.update({'id_equipamento':data['nome_equipamento']})
                    message_dict.update({'data_captura': data['data_captura']})
                    message_dict.update({'hora_captura': data['hora_captura']})
                    message_dict.update({'captura_base': data['captura_base']})

                    verify = DeepFace.verify(
                        img1_path = file,
                        img2_path = dataset_file,
                        model_name = Configuration.MODEL_BACKEND,
                        detector_backend = Configuration.BACKEND_DETECTOR,
                        distance_metric = Configuration.DISTANCE_METRIC,
                        enforce_detection = Configuration.ENFORCE_DETECTION,
                    )
                    confirm = verify['verified']
                    if confirm == True:
                        # Expressão regular para corresponder ao padrão "/app/media/dataset/188/" e capturar "188"
                        pattern = r"/app/media/dataset/(\d+)/"
                        # Use re.search para encontrar a correspondência
                        match = re.search(pattern, str(dataset_file))
                        # Verifique se houve uma correspondência antes de acessar o grupo capturado
                        if match:
                            dataset_id = match.group(1)  # Captura o valor "188"
                            message_dict.update({'aluno_id': dataset_id})

                        path_dataset = dataset_file.replace('/app/', '')
                        message_dict.update({'file_dataset': str(path_dataset)})
                        message_dict.update({'verify' : str(confirm)})

                        message_str = json.dumps(message_dict)
                        logger.debug(f' <*_ConsumerEmbbeding_*>DeepFace:: {message_str} ')
                        self.publisher.start_publisher(exchange = Configuration.RMQ_EXCHANGE,
                                                        queue_name = Configuration.RMQ_QUEUE_PUBLISHIR,
                                                        routing_name = Configuration.RMQ_ROUTE_KEY, 
                                                        message = message_str
                                                    )
                        self.db_connection.update(Configuration.UPDATE_QUERY, ('F', id_procesamento))
                        self.db_connection.insert(Configuration.INSER_QUERY, (dt.now(), dt.now(), id_procesamento, file, Configuration.BACKEND_DETECTOR, Configuration.MODEL_BACKEND, Configuration.DISTANCE_METRIC, confirm))



            except Exception as e:
                logger.error(f'<**ConsumerEmbbeding**> process_message :: {str(e)}')

if __name__ == "__main__":
    job = ConsumerFrequency()
    job.run()
import pika
import re
import json
import time
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
    RMQ_QUEUE_CONSUMER = 'faces'
    RMQ_QUEUE_PUBLISHIR = 'embedding'
    RMQ_ROUTE_KEY = 'verify'
    RMQ_RETRY_QUEUE = 'retry'

    DIR_CAPTURE = '/app/media/capturas/'
    DIR_DATASET = '/app/media/dataset/'

    MODEL_BACKEND = 'Facenet'
    BACKEND_DETECTOR = 'mtcnn'


    UPDATE_QUERY = """
        UPDATE 
            cameras_faces 
        SET 
            status = %s WHERE id = %s
    """

    INSER_QUERY = """
        INSERT INTO cameras_frequenciasescolar (
            data_cadastro,
            data_atualizacao,
            data,
            pessoa_id,
            camera_id
          )
        
        VALUES 
            (%s, %s, %s, %s, %s)
    """

class ConsumerEmbedding:
    def __init__(self):
        logger.info(f' <**ConsumerEmbbeding**> : Init ')
        self.reconnect_attempts = 0  # Adicione uma contagem de tentativas de reconexão
        self.max_reconnect_attempts = 3  # Defina um limite de tentativas de reconexão
        self.reconnecting = False
        self.connection = None
        self.channel = None

        self.redis_client = redis.Redis(
            host = Configuration.REDIS_SERVER, 
            port = Configuration.REDIS_PORT, 
            db = Configuration.REDIS_DB, 
            ssl = Configuration.REDIS_SSL
        )
        self.publisher = Publisher()
        self.db_connection = DatabaseConnection()

    def connect_to_rabbitmq(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=Configuration.RMQ_SERVER,
                    port=Configuration.RMQ_PORT,
                    credentials=pika.PlainCredentials(Configuration.RMQ_USER, Configuration.RMQ_PASS),
                    heartbeat=6000
                )
            )
            self.channel = self.connection.channel()
            self.channel.queue_bind(
                queue = Configuration.RMQ_QUEUE_PUBLISHIR,
                exchange = Configuration.RMQ_EXCHANGE,
                routing_key = Configuration.RMQ_ROUTE_KEY
            )
            self.channel.basic_consume(
                queue = Configuration.RMQ_QUEUE_CONSUMER,
                on_message_callback = self.process_message,
            )
            
            self.reconnect_attempts = 0  # Redefina a contagem de tentativas após uma conexão bem-sucedida
            self.reconnecting = False
        except Exception as e:
            error_message = f"Erro de conexão ao RabbitMQ: {str(e)}"
            logger.error(f'<*_ConsumerExtractor_*> Connection Error: {error_message}')
            self.reconnecting = True

    def run(self):
        while True:
            logger.info(f' <**ConsumerEmbbeding**> : start RUN FUNCTION')
            try:
                if not self.reconnecting:
                    self.connect_to_rabbitmq()

                self.channel.start_consuming()
            except KeyboardInterrupt:
                self.channel.stop_consuming()
            except Exception as e:
                message = f'error do tipo {type(e).__name__} com mensagem {str(e)}'
                logger.error(f' <**_**> ConsumerEmbbeding: Exception : {message}')
                self.reconnect_attempts += 1
                if self.reconnect_attempts <= self.max_reconnect_attempts:
                    time.sleep(2)
                else:
                    logger.error("Máximo de tentativas de reconexão atingido. Saindo.")
                    break
            finally:
                if self.db_connection.is_connected():
                    self.db_connection.close()
                if self.redis_client.connection_pool:
                    self.redis_client.connection_pool.disconnect()
                    self.redis_client.close()
                logger.error(f' <**_**> ConsumerEmbbeding: finally RUN FUNCTION')

    def process_message(self, ch, method, properties, body):
            data = json.loads(body)
            file = data['caminho_do_face']
            camera_id = data['equipamento']
            
            if file.endswith(('.jpg', '.jpeg', '.png')):
                id_procesamento = data['id_procesamento']
                data_captura = data['data_captura']
                date_time_captura = dt.strptime(f'{data_captura}', '%Y-%m-%d')  
                message_dict = {
                    'id_equipamento': camera_id,
                    'id_procesamento': id_procesamento,
                    'data_captura': data_captura,
                    'hora_captura': data['hora_captura'],
                    'captura_base': data['captura_base'],
                    'caminho_do_face': file,
                    'detector_backend': Configuration.BACKEND_DETECTOR,
                    'model_detector': Configuration.MODEL_BACKEND,
                    'metrics': Configuration.DISTANCE_METRIC,
                    'normalization': Configuration.MODEL_BACKEND
                }

                try:
                    target_embedding = DeepFace.represent(
                        img_path = file,
                        model_name = Configuration.MODEL_BACKEND,
                        detector_backend = Configuration.BACKEND_DETECTOR,
                        enforce_detection = Configuration.ENFORCE_DETECTION,
                        normalization=Configuration.MODEL_BACKEND
                    )[0]["embedding"]

                    query_vector = np.array(target_embedding).astype(np.float32).tobytes()

                    k = 2
                    base_query = f"*=>[KNN {k} @embedding $query_vector AS distance]"
                    query = Query(base_query).return_fields("distance").sort_by("distance").dialect(2)
                    results = self.redis_client.ft().search(query, query_params={"query_vector": query_vector})
                    
                    for idx, result in enumerate(results.docs):
                        logger.info(f"Index:: {idx+1} mais próximo {result.id} com distância {result.distance}")

                        dataset_file = str(result.id)
                    

                        verify = DeepFace.verify(
                            img1_path = file,
                            img2_path = dataset_file,
                            model_name = Configuration.MODEL_BACKEND,
                            detector_backend = Configuration.BACKEND_DETECTOR,
                            distance_metric = Configuration.DISTANCE_METRIC,
                            normalization=Configuration.MODEL_BACKEND
                        )
                        logger.info(f"Index:: {result.id} Verify:: {verify['verified']}")
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
                            logger.debug(f' <*_ConsumerEmbbeding_*>Mensagem:: {message_str} ')
                            self.publisher.start_publisher(exchange = Configuration.RMQ_EXCHANGE,
                                                            queue_name = Configuration.RMQ_QUEUE_PUBLISHIR,
                                                            routing_name = Configuration.RMQ_ROUTE_KEY, 
                                                            message = message_str
                                                        )
            
                            self.db_connection.update(Configuration.UPDATE_QUERY, ('Processado', id_procesamento))
                            self.db_connection.insert(Configuration.INSER_QUERY, (dt.now(), dt.now(), date_time_captura, int(dataset_id), int(camera_id) ))

                    self.channel.basic_ack(delivery_tag=method.delivery_tag)

                except Exception as e:
                    logger.error(f'<**ConsumerEmbbeding**> process_message :: {str(e)}')
                    #self.channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
                    self.channel.basic_ack(delivery_tag=method.delivery_tag)
                    self.db_connection.update(Configuration.UPDATE_QUERY, ('Processado', id_procesamento))

if __name__ == "__main__":
    job = ConsumerEmbedding()
    job.run()
import pika
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
    RMQ_QUEUE_CONSUMER = 'analizy'

    DIR_CAPTURE = '/app/media/capturas/'
    DIR_DATASET = '/app/media/dataset/'


    INSER_QUERY = """
        INSERT INTO analytical_facesprevisaoemocional (
            data_cadastro,
            data_atualizacao,
            predominante,
            zangado,
            repulsa,
            medo,
            feliz,
            neutro,
            triste,
            surpresa,
            face_id
          )
        VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

class ConsumerAnalizy:
    def __init__(self):
        logger.info(f' <**ConsumerEmbbeding**> : Init ')
        self.reconnect_attempts = 0  # Adicione uma contagem de tentativas de reconexão
        self.max_reconnect_attempts = 3  # Defina um limite de tentativas de reconexão
        self.reconnecting = False
        self.connection = None
        self.channel = None
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
                logger.error(f' <**_**> ConsumerEmbbeding: finally RUN FUNCTION')

    def process_message(self, ch, method, properties, body):
            data = json.loads(body)
            file = data['caminho_do_face']
            
            if file.endswith(('.jpg', '.jpeg', '.png')):
                print(file)
                try:
                    analizado = DeepFace.analyze(img_path=file, actions=['emotion'])
                    json_analizy = json.loads(analizado)
                    print(json_analizy)
                    #[
                    # {
                    # 'emotion': {'
                    # angry': 0.14176625991240144, 
                    # 'disgust': 1.064139141249143e-05, 
                    # 'fear': 0.0019596496713347733, 
                    # 'happy': 99.65722560882568, 
                    # 'sad': 0.07404087809845805, 
                    # 'surprise': 0.0035963741538580507, 
                    # 'neutral': 0.12140091275796294}, 
                    #'dominant_emotion': 'happy', 
                    # 'region': {'x': 3, 'y': 100, 'w': 65, 'h': 65}, 
                    # 'face_confidence': 4.39553095161682
                    # }
                    # ]
 

                    #self.channel.basic_ack(delivery_tag=method.delivery_tag)

                except Exception as e:
                    logger.error(f'<**ConsumerEmbbeding**> process_message :: {str(e)}')
                    self.channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

if __name__ == "__main__":
    job = ConsumerAnalizy()
    job.run()
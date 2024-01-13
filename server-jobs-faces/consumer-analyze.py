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

    SELECT_QUERY = """
        SELECT
            id
        FROM
            cameras_faces
        WHERE
           path_face = %s
    """


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
            surpresa          
        )
        VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

class ConsumerAnalyze:
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
                try:
                    emotion = DeepFace.analyze(img_path=file, actions=['emotion'])
                    # Para acessar o dicionário de emoção:
                    emotion_dict = emotion[0]['emotion']
                    dominant_emotion = emotion[0]['dominant_emotion']

                    logger.debug(f'<**ConsumerEmbbeding**> Emocoes :: {emotion_dict}')
                    logger.debug(f'<**ConsumerEmbbeding**> Emocao Dominante :: {dominant_emotion}')
                    # Em seguida, você pode acessar campos dentro do dicionário de emoção, por exemplo, o valor de 'angry':

                    
                    angry_value = format(emotion_dict['angry'],'.2f')
                    disgust_value = format(emotion_dict['disgust'],'.2f')
                    fear_value = format(emotion_dict['fear'],'.2f')
                    happy_value = format(emotion_dict['happy'],'.2f')
                    sad_value = format(emotion_dict['sad'],'.2f')
                    surprise_value = format(emotion_dict['surprise'],'.2f')
                    neutral_value = format(emotion_dict['neutral'],'.2f')
                    
                    logger.debug(f'<**ConsumerEmbbeding**> FLOATS :: {angry_value} - {disgust_value} - {fear_value} - {happy_value} - {sad_value} - {surprise_value} - {neutral_value}')


                    self.db_connection.insert(Configuration.INSER_QUERY, (
                        dt.now(), 
                        dt.now(),
                        dominant_emotion,
                        angry_value,
                        disgust_value,
                        fear_value,
                        happy_value,
                        neutral_value,
                        sad_value,
                        surprise_value
                        )
                    )

                    self.channel.basic_ack(delivery_tag=method.delivery_tag)

                except Exception as e:
                    logger.error(f'<**ConsumerEmbbeding**> Error :: {str(e)}')
                    self.channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

if __name__ == "__main__":
    job = ConsumerAnalyze()
    job.run()
import pika
import json
import os
import cv2
from datetime import datetime as dt
from conectionDB import DatabaseConnection
from publicar import Publisher
from loggingMe import logger
from deepface import DeepFace

class Configuration:
    RMQ_SERVER = 'broker-server'
    RMQ_PORT = 5672
    RMQ_EXCHANGE = 'secedu'
    RMQ_QUEUE_PUBLISHIR = 'faces'
    RMQ_ROUTE_KEY = 'extrair'
    RMQ_QUEUE_CONSUMER = 'ftp'
    RMQ_ASK_DEBUG = True
    BACKEND_DETECTOR = 'retinaface'
    MODEL_BACKEND = 'Facenet'
    DISTANCE_METRIC = 'euclidean_l2'
    LIMITE_DETECTOR = 0.96
    LIMITE_AREA = 80
    DIR_CAPTURE = '/app/media/capturas'
    UPDATE_QUERY = """
            UPDATE cameras_processamentos
            SET status = %s
            WHERE id = %s
        """

class ConsumerExtractor:
    def __init__(self):
        self.path_capture = Configuration.DIR_CAPTURE
        self.backend_detector = Configuration.BACKEND_DETECTOR
        self.model_backend = Configuration.MODEL_BACKEND
        self.distance_metric = Configuration.DISTANCE_METRIC
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=Configuration.RMQ_SERVER,
                port=Configuration.RMQ_PORT,
                credentials=pika.PlainCredentials('secedu', 'ep4X1!br')
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_bind(
            queue=Configuration.RMQ_QUEUE_PUBLISHIR,
            exchange=Configuration.RMQ_EXCHANGE,
            routing_key=Configuration.RMQ_ROUTE_KEY
        )
        self.publisher = Publisher()
        self.db_connection = DatabaseConnection()

    def run(self):
        logger.debug('<*_ConsumerExtractor_*> Run Init')
        self.channel.basic_consume(
            queue=Configuration.RMQ_QUEUE_CONSUMER,
            on_message_callback=self.process_message,
            auto_ack=Configuration.RMQ_ASK_DEBUG
        )
        try:
            self.db_connection.connect()
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
        except Exception as e:
            logger.error(f'<*_ConsumerExtractor_*> Exception:Run: {e}')
        finally:
            logger.debug('<*_ConsumerExtractor_*> Finally:Run:')
            self.connection.close()
            self.publisher.close()
            self.db_connection.close()


    def process_message(self, ch, method, properties, body):
        data = json.loads(body)
        file = data['path_file']
        horario = data['horario']
        device = data['local']

        id_procesamento = data['proccess_id']

        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            now = dt.now()
            equipamento = data['nome_equipamento']
            data_captura = data['data_captura']
            processamento = now.strftime("%Y-%m-%d %H:%M:%S")
            message_dict = {
                'data_processo': processamento,
                'data_captura': data_captura,
                'hora_captura': horario,
                'nome_equipamento': equipamento,
                'local_equipamento': device,
                'captura_base': file,
                'proccess_id': id_procesamento
            }

            try:
                face_objs = DeepFace.extract_faces(
                    img_path=file,
                    detector_backend=self.backend_detector,
                    enforce_detection=False,
                    align=True
                )

                for index, face_obj in enumerate(face_objs):
                    area = (face_obj['facial_area']['h'] + face_obj['facial_area']['w']) / 2
                    confidence = face_obj['confidence']
                    logger.debug(f'<*_ConsumerExtractor_*> ProcessMessage:Area: {area} confidence:: {confidence}')
                    if confidence >= Configuration.LIMITE_DETECTOR and area >= Configuration.LIMITE_AREA:
                        face = face_obj['face']
                        new_face = os.path.join(str(self.path_capture), str(equipamento), str(data_captura), str(horario))

                        if not os.path.exists(new_face):
                            os.makedirs(new_face, exist_ok=True)

                        face_uint8 = (face * 255).astype('uint8')
                        save_path = os.path.join(new_face, f"face_{index}_noises.jpg")
                        cv2.imwrite(save_path, cv2.cvtColor(face_uint8, cv2.COLOR_RGB2BGR))

                        message_dict.update({'caminho_do_face': save_path})
                        message_dict.update({'area': area})
                        message_dict.update({'confidence': confidence})
                        message_dict.update({'detector_backend': self.backend_detector})
                        message_dict.update({'model_backend': self.model_backend})
                        message_str = json.dumps(message_dict)
                        self.publisher.start_publisher(exchange=Configuration.RMQ_EXCHANGE, 
                                                       routing_name=Configuration.RMQ_ROUTE_KEY, 
                                                       message=message_str
                                                    )
                        self.db_connection.update(Configuration.UPDATE_QUERY, ('Processado', id_procesamento))
                        logger.debug(f'<*_ConsumerExtractor_*> ProccessMessage:MENSSAGEM JSON: {message_str}')
                
            except Exception as e:
                self.db_connection.update(Configuration.UPDATE_QUERY, ('Error', id_procesamento))
                logger.error(f'<*_ConsumerExtractor_*> Try:New Face: {e}')

if __name__ == "__main__":
    job = ConsumerExtractor()
    job.run()

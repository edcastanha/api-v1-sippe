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
    RMQ_USER = 'secedu'
    RMQ_PASS = 'ep4X1!br'
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

class ConsumerExtractor:
    def __init__(self):
        self.path_capture = Configuration.DIR_CAPTURE
        self.model_backend = Configuration.MODEL_BACKEND
        self.distance_metric = Configuration.DISTANCE_METRIC
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host = Configuration.RMQ_SERVER,
                port = Configuration.RMQ_PORT,
                credentials = pika.PlainCredentials(Configuration.RMQ_USER, Configuration.RMQ_PASS)
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_bind(
            queue = Configuration.RMQ_QUEUE_PUBLISHIR,
            exchange = Configuration.RMQ_EXCHANGE,
            routing_key = Configuration.RMQ_ROUTE_KEY
        )
        self.publisher = Publisher()
        self.db_connection = DatabaseConnection()

    def run(self):
        logger.debug('<*_ConsumerExtractor_*> Run Init')
        self.channel.basic_consume(
            queue = Configuration.RMQ_QUEUE_CONSUMER,
            on_message_callback = self.process_message,
            auto_ack = Configuration.RMQ_ASK_DEBUG
        )
        try:
            self.db_connection.connect()
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
        except Exception as e:
            logger.error(f'<*_ConsumerExtractor_*> Exception-Run : Error::{e}')
        finally:
            logger.debug('<*_ConsumerExtractor_*> Finally : Run:')
            if self.connection.is_open:
                self.connection.close()
            self.publisher.close()
            self.db_connection.close()


    def process_message(self, ch, method, properties, body):
        data = json.loads(body)
        try:
            logger.debug(f'<*_ConsumerExtractor_*> ProcessMessage: JSON{data}')
            if 'path_file' and 'proccess_id' in data  :
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

                    
                    face_objs = DeepFace.extract_faces(
                        img_path=file,
                        detector_backend=Configuration.BACKEND_DETECTOR,
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
                            message_dict.update({'detector_backend': Configuration.BACKEND_DETECTOR})
                            message_str = json.dumps(message_dict)
                            get_publisher = self.publisher.start_publisher(exchange=Configuration.RMQ_EXCHANGE, 
                                                            routing_name=Configuration.RMQ_ROUTE_KEY, 
                                                            message=message_str
                                                        )

                            values =  (dt.now(), dt.now(), int(id_procesamento), save_path, Configuration.BACKEND_DETECTOR, Configuration.MODEL_BACKEND, Configuration.DISTANCE_METRIC, False)

                            get_update = self.db_connection.update(Configuration.UPDATE_QUERY, ('Processado', id_procesamento))
                            get_insert = self.db_connection.insert(Configuration.INSER_QUERY, values)
                            logger.debug(f'<*_ConsumerExtractor_*> ProccessMessage - Pub={get_publisher}:Up={get_update}:Ins={get_insert}')
                    
        except Exception as e:
            self.db_connection.update(Configuration.UPDATE_QUERY, ('Error', data['proccess_id']))
            logger.error(f'<*_ConsumerExtractor_*> Try:New Face: {e}')
        finally:
            logger.debug('<*_ConsumerExtractor_*> Finally:ProcessMessage')
            

if __name__ == "__main__":
    job = ConsumerExtractor()
    job.run()

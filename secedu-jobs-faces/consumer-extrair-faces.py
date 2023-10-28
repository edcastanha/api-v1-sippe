import pika
import json
import os
import cv2
from datetime import datetime as dt
from conectionDB import DatabaseConnection
from publicar import Publisher
from loggingMe import logger
from deepface import DeepFace
from configuration import Configuration as config

class Configuration(config):
    RMQ_QUEUE_PUBLISHIR = 'faces'
    RMQ_ROUTE_KEY = 'init'
    RMQ_QUEUE_CONSUMER = 'ftp'
    RMQ_ASK_DEBUG = True
    
    DIR_CAPTURE = '/app/media/capturas'
    
    UPDATE_QUERY = """
        UPDATE 
            cameras_processamentos 
        SET 
            status = %s WHERE id = %s
    """
    INSER_QUERY = """
        INSERT INTO cameras_faces (
            data_cadastro,
            data_atualizacao,
            path_face,
            backend_detector,
            auditado,
            processamento_id
          )
        VALUES (
           %s, %s, %s, %s, %s, %s
           )
    """

class ConsumerExtractor:
    def __init__(self):
        self.path_capture = Configuration.DIR_CAPTURE
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
        self.channel.basic_consume(
            queue = Configuration.RMQ_QUEUE_CONSUMER,
            on_message_callback = self.process_message,
            auto_ack = Configuration.RMQ_ASK_DEBUG
        )
        self.publisher = Publisher()
        self.db_connection = DatabaseConnection()

    def run(self):
        logger.debug('<*_ConsumerExtractor_*> Run - Init')
        
        try:
            self.db_connection.connect()
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
        except Exception as e:
            logger.error(f'<*_ConsumerExtractor_*> Exception-Run : Error::{e}')
        finally:
            logger.debug('<*_ConsumerExtractor_*> Run - Finally :')
            if self.connection.is_open:
                self.connection.close()
            if self.db_connection.is_connected():
                self.db_connection.close()


    def process_message(self, ch, method, properties, body):
        data = json.loads(body)
        try:
            logger.debug(f'<*_ConsumerExtractor_*> ProcessMessage: JSON{data}')
            if 'path_file' in data and 'proccess_id' in data  :
                file = data['path_file']
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    now = dt.now()
                    horario = data['horario']
                    device = data['local']
                    id_procesamento = data['proccess_id']
                    equipamento = data['nome_equipamento']
                    data_captura = data['data_captura']
                    message_dict = {
                        'data_captura': data_captura,
                        'hora_captura': horario,
                        'nome_equipamento': equipamento,
                        'local_equipamento': device,
                        'captura_base': file,
                        'id_procesamento': id_procesamento
                    }

                    
                    face_objs = DeepFace.extract_faces(
                        img_path=file,
                        detector_backend=Configuration.BACKEND_DETECTOR,
                        enforce_detection=Configuration.ENFORCE_DETECTION,
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

                            # Aplique a filtragem bilateral
                            save_filter = os.path.join(new_face, f"face_{index}_filter.jpg")
                            # Aplique a filtragem de mediana com um tamanho de kernel (por exemplo: 3x3, 5x5 ou 7x7)
                            imagem_filtrada = cv2.medianBlur(face_uint8, 3)  # Ajuste o tamanho do kernel conforme necessário
                            imagem_suavizada = cv2.bilateralFilter(imagem_filtrada, d=5, sigmaColor=35, sigmaSpace=65)

                            cv2.imwrite(save_filter, cv2.cvtColor(imagem_suavizada, cv2.COLOR_RGB2BGR))


                            if not os.path.exists(save_path):
                                raise Exception(f'Não foi possível salvar a imagem {save_path}')
                            
                            message_dict.update({'caminho_do_face': save_path})
                            message_dict.update({'area': area})
                            message_dict.update({'confidence': confidence})
                            message_dict.update({'detector_backend': Configuration.BACKEND_DETECTOR})
                            message_str = json.dumps(message_dict)
                            db_path = save_path.replace('/app/', '')
                            
                            get_publisher = self.publisher.start_publisher(exchange=Configuration.RMQ_EXCHANGE, 
                                                            queue_name=Configuration.RMQ_QUEUE_PUBLISHIR,
                                                            routing_name=Configuration.RMQ_ROUTE_KEY, 
                                                            message=message_str
                                                        )
                            # Update Processos -  status de Criado para Processado
                            get_update = self.db_connection.update(Configuration.UPDATE_QUERY, ('Processado', id_procesamento))
                           
                           # Insert Faces
                            values =  (dt.now(), dt.now(), db_path, Configuration.BACKEND_DETECTOR, False, id_procesamento)
                            get_insert = self.db_connection.insert(Configuration.INSER_QUERY, values)
                            
                            logger.debug(f'<*_ConsumerExtractor_*> ProccessMessage - Pub={get_publisher}:Up={get_update}:Ins={get_insert}')
                    
        except Exception as e:
            error_message = f"An exception of type {type(e).__name__} occurred with the message: {str(e)}"
            logger.error(f'<*_ConsumerExtractor_*> New Face: {error_message}')
            self.db_connection.update(Configuration.UPDATE_QUERY, ('Error', data['proccess_id']))
        finally:
            logger.debug('<*_ConsumerExtractor_*> Finally - ProcessMessage')
            
if __name__ == "__main__":
    job = ConsumerExtractor()
    job.run()

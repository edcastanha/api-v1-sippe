import pika
import json
import time
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
    RMQ_RETRY_QUEUE = 'retry' 
    RMQ_RETRY_ROUTE= 'ftp_retry'
    
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
        self.reconnect_attempts = 0  # Adicione uma contagem de tentativas de reconexão
        self.max_reconnect_attempts = 3  # Defina um limite de tentativas de reconexão
        self.path_capture = Configuration.DIR_CAPTURE
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
                    credentials=pika.PlainCredentials(
                        Configuration.RMQ_USER,
                        Configuration.RMQ_PASS),
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
            logger.debug('<*_ConsumerExtractor_*> Run - Init')
            try:
                if not self.reconnecting:
                    self.connect_to_rabbitmq()

                self.channel.start_consuming()
            except KeyboardInterrupt:
                self.channel.stop_consuming()
            except Exception as e:
                error_message = f"Uma exceção do tipo {type(e).__name__} ocorreu com a mensagem: {str(e)}"
                logger.error(f'<*_ConsumerExtractor_*> Exception-Run: {error_message}')
                self.reconnect_attempts += 1
                if self.reconnect_attempts <= self.max_reconnect_attempts:
                    time.sleep(2)
            finally:
                #Postgres Connection
                if self.db_connection.is_connected():
                    self.db_connection.close()
                    #logger.debug('<*_ConsumerExtractor_*> Run - DB Connection Close')
                logger.debug('<*_ConsumerExtractor_*> Run - Finally :')

    def process_message(self, ch, method, properties, body):
        data = json.loads(body)
        file = data['path_file']
        id_procesamento = int(data['id_procesamento'])
        self.db_connection.connect()
        if 'path_file' in data and 'id_procesamento' in data and file.lower().endswith(('.jpg', '.jpeg', '.png')):
            try:
                now = dt.now()
                horario = str(data['horario'])
                # Extrair horas, minutos e segundos usando fatiamento
                hora = horario[:2]
                minuto = horario[3:5]
                segundo = horario[6:8]
                #logger.debug(f'<*_ConsumerExtractor_*> ProcessMessage: Hora:{hora} Minuto:{minuto} Segundo:{segundo}')
                equipamento = data['nome_equipamento']
                data_captura = data['data_captura']
                message_dict = {
                    'data_captura': data_captura,
                    'hora_captura': horario,
                    'equipamento': equipamento,
                    'captura_base': file,
                    'id_procesamento': id_procesamento
                }

                face_objs = DeepFace.extract_faces(
                    img_path=file,
                    detector_backend=Configuration.BACKEND_DETECTOR,
                    enforce_detection=Configuration.ENFORCE_DETECTION,
                    align=True
                )

                if len(face_objs) > 0:
                    for index, face_obj in enumerate(face_objs):
                        area = (face_obj['facial_area']['h'] + face_obj['facial_area']['w']) / 2
                        confidence = face_obj['confidence']
                                                
                        if confidence >= Configuration.LIMITE_DETECTOR and area >= Configuration.LIMITE_AREA:
                            face = face_obj['face']
                            new_face = os.path.join(self.path_capture, str(equipamento), data_captura,hora, minuto)

                            if not os.path.exists(new_face):
                                os.makedirs(new_face, exist_ok=True)

                            face_uint8 = (face * 255).astype('uint8')
                        
                            save_path = os.path.join(new_face, f"{segundo}s_face_{index}.jpg")
                            #cv2.imwrite(save_path, cv2.cvtColor(face_uint8, cv2.COLOR_RGB2BGR))

                            # Aplique a filtragem bilateral
                            # Aplique a filtragem de mediana com um tamanho de kernel (por exemplo: 3x3, 5x5 ou 7x7)
                            imagem_filtrada = cv2.medianBlur(face_uint8, 3)  # Ajuste o tamanho do kernel conforme necessário
                            imagem_suavizada = cv2.bilateralFilter(imagem_filtrada, d=5, sigmaColor=35, sigmaSpace=65)

                            cv2.imwrite(save_path, cv2.cvtColor(imagem_suavizada, cv2.COLOR_RGB2BGR))
                            
                            message_dict.update({'caminho_do_face': save_path})
                            message_dict.update({'area': area})
                            message_dict.update({'confidence': confidence})
                            message_dict.update({'detector_backend': Configuration.BACKEND_DETECTOR})
                            message_str = json.dumps(message_dict)
                            db_path = save_path.replace('/app/', '')

                            values =  (now, now, db_path, Configuration.BACKEND_DETECTOR, False, id_procesamento)
                            self.db_connection.update(Configuration.UPDATE_QUERY, ('Enviado', id_procesamento))
                            self.db_connection.insert(Configuration.INSER_QUERY, values)

                            self.publisher.start_publisher(exchange=Configuration.RMQ_EXCHANGE, 
                                                        queue_name=Configuration.RMQ_QUEUE_PUBLISHIR,
                                                        routing_name=Configuration.RMQ_ROUTE_KEY, 
                                                        message=message_str
                                                    )
                    # Update Status Processamento -  Enviado devido localizado face`s
                    self.db_connection.update(Configuration.UPDATE_QUERY, ('Enviado', id_procesamento))

                            
                # Update Status Processamento -  Processado devido nao haver faces
                self.db_connection.update(Configuration.UPDATE_QUERY, ('Processado', id_procesamento))
                    
            except Exception as e:
                self.db_connection.update(Configuration.UPDATE_QUERY, ('Error', id_procesamento))

                error_message = f"Uma exceção do tipo {type(e).__name__} ocorreu com a mensagem: {str(e)}"
                logger.error(f'<*_ConsumerExtractor_*> Process_Message: {error_message}')
                self.channel.basic_nack(method.delivery_tag, requeue=True)  
            finally:
                self.channel.basic_ack(method.delivery_tag)
                logger.info(f'<*_ConsumerExtractor_*> Process_Message - Finish')
         
if __name__ == "__main__":
    job = ConsumerExtractor()
    job.run()

import pika
import json
from datetime import datetime as dt
import os
import re
import numpy as np
import uuid
import cv2
import mediapipe as mp

import redis
from redis.commands.search.field import VectorField, TagField
from redis.commands.search.query import Query

from deepface import DeepFace
from publicar import Publisher
from loggingMe import logger

REDIS_SERVER = 'redis-server'
RMQ_SERVER = 'broker-server'

EXCHANGE='secedu'
QUEUE_PUBLISHIR='faces'
ROUTE_KEY='extractor'

QUEUE_CONSUMER='ftp'
ASK_DEBUG = True

DIR_CAPS ='media/capturas'

BACKEND_DETECTOR='mediapipe'
#MODEL_BACKEND ='mtcnn'
MODEL_BACKEND ='Facenet'
LIMITE_DETECTOR = 0.99

from os import environ

DeepFace.build_model(MODEL_BACKEND)

r = redis.StrictRedis(host=REDIS_SERVER, port=6379, db=0)

logger.debug(f' <**_ 1 _**> RMQ_SERVER::{RMQ_SERVER}')

class ConsumerExtractor:
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

    def run(self):
        logger.debug(f' <**_**> ConsumerExtractor: Aguardando {QUEUE_CONSUMER}')
        self.channel.basic_consume(
            queue=QUEUE_CONSUMER,
            on_message_callback=self.process_message,
            auto_ack=ASK_DEBUG
        )

        try:
            self.channel.start_consuming()
            logger.debug(f' <**_**> ConsumerExtractor: start_consumer')
        finally:
            self.connection.close()
            logger.debug(f' <**_**> ConsumerExtractor: close')

    def process_message(self, ch, method, properties, body):
        data = json.loads(body)
        file = data['path_file']
        horario = data['horario']
        device = data['local']
        logger.debug(f' <**_**> ConsumerExtractor: 1 process_message:: {data}')

        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            now = dt.now()
            equipamento =data['nome_equipamento']
            data_captura=data['data_captura']
            proccess = now.strftime("%Y-%m-%d %H:%M:%S")
            message_dict = {
                'data_processo': proccess,
                'data_captura': data_captura,
                'hora_captura': horario,
                'nome_equipamento': equipamento,
                'local_equipamento': device,
                'captura_base': file,
            }
            logger.debug(f' <**_**> ConsumerExtractor: 2 process_message:: {message_dict}')
            
            face_objs = DeepFace.extract_faces(img_path=file,
                                               detector_backend=BACKEND_DETECTOR,
                                               enforce_detection=False,
                                               align=True
                                               )
            try:
                for index, face_obj in enumerate(face_objs):
                    if face_obj['confidence'] >= LIMITE_DETECTOR:
                        face = face_obj['face']
                        new_face = os.path.join(str(DIR_CAPS), str(equipamento), str(data_captura), str(horario))

                        if not os.path.exists(new_face):
                            os.makedirs(new_face, exist_ok=True)

                        # Converta a imagem de float32 para uint8 (formato de imagem)
                        face_uint8 = (face * 255).astype('uint8')
                        
                        # Gere um nome de arquivo único para a face
                        save_path = os.path.join(new_face, f"face_{index}.jpg")
                        logger.debug(f' <**SAVE NEW FACE**> 3 Path:: {save_path}: ')
                        
                        
                        # Salve a face no diretório "captura/" usando OpenCV
                        cv2.imwrite(save_path, cv2.cvtColor(face_uint8, cv2.COLOR_RGB2BGR))
                        self.analyze_mediapipe(save_path,)
                        publisher = Publisher()
                        message_dict.update({'caminho_do_face': save_path})
                        message_dict.update({'detector_backend': BACKEND_DETECTOR})
                        message_str = json.dumps(message_dict)
                        publisher.start_publisher(exchange=EXCHANGE, routing_name=ROUTE_KEY, message=message_str)
                        publisher.close()
                        pipeline = r.pipeline(transaction=False)
                        pipeline.hset(save_path, mapping={"message": message_str})
                        pipeline_results = pipeline.execute()
                        logger.debug(f' <**_ REDIS _**> 4 PIPELINE :: {pipeline_results}')
            except Exception as e:
                logger.debug(f' <**EXTRATOR FACE**> 3 Erro:: {e}')

    def analyze_mediapipe(img_path, actions, detector_backend, enforce_detection, align):
        result = {}
        mp_face_mesh = mp.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)
        img = cv2.imread(img_path)

        results = face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0]
        # Faça o que você precisa com os landmarks
        
            df = pd.DataFrame(list(mp_face_mesh.FACEMESH_FACE_OVAL), columns=["p1", "p2"])
            print(f"A face oval é constituída por {df.shape[0]} linhas")
            routes_idx = []

            p1 = df.iloc[0]["p1"]
            p2 = df.iloc[0]["p2"]

            for i in range(0, df.shape[0]):
                obj = df[df["p1"] == p2]
                p1 = obj["p1"].values[0]
                p2 = obj["p2"].values[0]

                route_idx = []
                route_idx.append(p1)
                route_idx.append(p2)
                routes_idx.append(route_idx)

            # Encontrar os valores das coordenadas 2D de cada ponto de referência
            routes = []

            for source_idx, target_idx in routes_idx:
                source = landmarks.landmark[source_idx]
                target = landmarks.landmark[target_idx]

                relative_source = (int(img.shape[1] * source.x), int(img.shape[0] * source.y))
                relative_target = (int(img.shape[1] * target.x), int(img.shape[0] * target.y))

                routes.append(relative_source)
                routes.append(relative_target)

            # Extrair a área interior dos pontos de referência faciais
            mask = np.zeros((img.shape[0], img.shape[1]))
            mask = cv2.fillConvexPoly(mask, np.array(routes), 1)
            mask = mask.astype(bool)

            out = np.zeros_like(img)
            out[mask] = img[mask]

        
            # Verificar se o diretório 'capturas/ovalFace/' existe e, se não, criá-lo
            save_dir = 'capturas/ovalFace/'
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            # Gerar um nome de arquivo aleatório
            random_filename = str(uuid.uuid4()) + '.png'
            path = os.path.join(save_dir, random_filename)
            # Salvar a imagem no diretório
            cv2.imwrite(path, out)

            
            demographies = DeepFace.analyze(
                img_path=path,
                actions=actions,
                detector_backend=detector_backend,
                enforce_detection=enforce_detection,
                align=align,
            )

            result["results"] = demographies

            result['face_location'] = path
            return result
        else:
            return {"results": "No face detected"}


    
if __name__ == "__main__":
    job = ConsumerExtractor()
    job.run()
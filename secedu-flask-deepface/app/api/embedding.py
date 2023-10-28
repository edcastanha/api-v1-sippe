import os
from deepface import DeepFace
from tqdm import tqdm
import redis
import json
import numpy as np
from redis.commands.search.field import VectorField

class Trainning:
    def __init__(self, redis_host='redis-server', redis_port=6379, redis_db=0):
        self.dir_db_img = '/app/media/dataset/'
        self.dir_face_oval = '/app/media/faces-oval/'
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.models = [
            "VGG-Face",       #0
            "Facenet",        #1
            "Facenet512",     #2
            "OpenFace",       #3
            "DeepFace",       #4
            "DeepID",         #5
            "ArcFace",        #6
            "Dlib",           #7
            "SFace",          #8
        ]
        self.detector = [
            "opencv",       #0
            "mtcnn",        #1
            "dlib",         #2
            "ssd",          #3
            "retinaface",   #4
            "arcface",      #5
            "mediapipe",    #6
        ]
        self.redis_client = redis.Redis(host=self.redis_host, port=self.redis_port, db=self.redis_db, ssl=False)
        self.representations = []

    def flush_redis(self):
        # Redis command Delete All Keys
        self.redis_client.flushall()

    def calculate_embedding(self, img_path):
        embedding_obj = DeepFace.represent(
            img_path=img_path, 
            model_name=self.models[1], 
            detector_backend=self.detector[4],
            enforce_detection=False,
            normalization=self.models[1]
        )
        print(embedding_obj)
        embedding = embedding_obj[0]["embedding"]
        return embedding

    def add_to_representations(self, img_path, embedding):
        self.representations.append((img_path, embedding))

    def add_to_redis(self,embeddings):
        pipeline = self.redis_client.pipeline(transaction=False)
        for img_path, embedding in tqdm(embeddings):
            value = np.array(embedding).astype(np.float32).tobytes()
            
            # store embedings into redis one by one
            #r.hset(key, mapping = {"embedding": value})
            
            # store embedings into redis in one shot
            pipeline.hset(img_path, mapping = {"embedding": value})

        pipeline_results = pipeline.execute()
        
        self.redis_client.ft().create_index(
            [
                VectorField(
                    "embedding",
                    "HNSW",
                    {
                        "TYPE": "FLOAT32",
                        "DIM": 128,
                        "DISTANCE_METRIC": "L2",
                    },
                )
            ]
        )

    def process_images(self):
        for dir_path, dir_names, file_names in os.walk(self.dir_db_img):
            for file_name in file_names:
                img_path = os.path.join(dir_path, file_name)
                if img_path.endswith((".png", ".jpg", ".jpeg")):
                    print(f'IMG:: {img_path}')
                    embedding = self.calculate_embedding(img_path)
                    self.add_to_representations(img_path, embedding)
                else:
                    print(f"Arquivo inválido ou extensão não suportada: {img_path}")
        
        self.add_to_redis(embeddings= self.representations)

        result = [key.decode('utf-8') for key in self.redis_client.keys()]
        
        return result

#if __name__ == "__main__":
#    trainning = Trainning()
#    trainning.flush_redis()
#    json_data = trainning.process_images()

 #   print(f'KEYS:: {json_data}')

import os
from deepface import DeepFace
from tqdm import tqdm
import redis
import json

class Trainning:
    #def __init__(self, dir_db_img, redis_host='localhost', redis_port=6379, redis_pass='ep4X1!br', redis_db=0, img_path='dataset'):
    def __init__(self, redis_host='redis-server', redis_port=6379, redis_db=0):
        self.dir_db_img = 'dataset/'
        self.redis_host = redis_host
        self.redis_port = redis_port
        #self.redis_pass = redis_pass
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
        #self.redis_client = redis.StrictRedis(host=self.redis_host, port=self.redis_port, password=self.redis_pass, db=self.redis_db)
        self.redis_client = redis.StrictRedis(host=self.redis_host, port=self.redis_port, db=self.redis_db)
        self.representations = []

    def flush_redis(self):
        self.redis_client.flushall()

    def calculate_embedding(self, img_path):
        embedding_obj = DeepFace.represent(
            img_path=img_path, 
            model_name=self.models[1], 
            detector_backend=self.detector[6],
            enforce_detection=False
        )
        embedding = embedding_obj[0]["embedding"]
        return embedding

    def add_to_representations(self, img_path, embedding):
        self.representations.append((img_path, embedding))

    def add_to_redis(self, img_path, embedding):
        self.redis_client.rpush(f"embedding:{img_path}", *embedding)

    def process_images(self):
        result= {}
        for dir_path, dir_names, file_names in os.walk(self.dir_db_img):
            for file_name in file_names:
                img_path = os.path.join(dir_path, file_name)
                if img_path.endswith((".png", ".jpg", ".jpeg")):
                    embedding = self.calculate_embedding(img_path)
                    self.add_to_representations(img_path, embedding)
                else:
                    print("Arquivo inválido ou extensão não suportada.")
        for img_path, embedding in self.representations:
            self.add_to_redis(img_path, embedding)

        print(self.redis_client.keys())
        
        # Suponha que 'my_bytes' seja o objeto bytes que você deseja serializar em JSON
        my_bytes = self.redis_client.keys()
        decoded_string = None
        # Verifique se my_bytes é uma lista de bytes
        if isinstance(my_bytes, list):
            # Itere sobre os elementos da lista e aplique decode a cada um
            decoded_string = [item.decode('utf-8') for item in my_bytes]
        else:
            # Trate o objeto my_bytes como um único objeto de bytes
            decoded_string = my_bytes.decode('utf-8')
        # Agora, você pode serializar a string em JSON
        json_data = json.dumps({'results': decoded_string})

        return json_data

#if __name__ == "__main__":
#    trainning = Trainning()
#    trainning.flush_redis()
#    trainning.process_images()
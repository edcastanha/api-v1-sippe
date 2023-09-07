from deepface import DeepFace
from tqdm import tqdm
import numpy as np
from deepface.commons import functions
#!pip install redis
import redis
redis = redis.StrictRedis(host='localhost', port=6379, db=0)

target_img_path = "mongo-target.jpg"
 
#detect and align
target_img = DeepFace.extract_faces(img_path = target_img_path)[0]["face"]
 
#represent
target_embedding = DeepFace.represent(img_path = target_img_path, model_name = "Facenet")[0]["embedding"]


def verify_face(key):
    embedding = redis.lrange('embedding:'+key, 0, -1)
     
    distance = findEuclideanDistance(target_embedding, np.array(embedding).astype('float'))
     
    if distance >= 10:
        print("this is "+key)
    else:
        print("this IS NOT "+key)
 
verify_face('angelina')

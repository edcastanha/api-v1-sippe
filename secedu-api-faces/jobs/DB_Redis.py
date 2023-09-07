import os
from deepface import DeepFace
import json
from tqdm import tqdm
 
#!pip install redis
import redis
redis = redis.StrictRedis(host='localhost', port=6379, db=0)

for key in redis.scan_iter("embedding:*"):
    redis.delete(key)
    print("Delete embedding:")

for key in redis.scan_iter("photo:*"):
    redis.delete(key)
    print("Delete dataset!")


DIR_FOTO = "C:/projetos/api-v1-sippe/api/medias/dataset"

identities = list(local_db.keys())
print("identities: ", identities)
for i in tqdm(range(0, len(identities))):
    name = identities[i]
    img_path = local_db[name]
     
    embedding = DeepFace.represent(img_path = img_path, model_name = "Facenet", detector_backend="retinaface",)[0]["embedding"]
    print(embedding)
    #store in redis
    redis.rpush("embedding:"+name, *embedding)
    redis.set("photo:"+name, img_path)
    print("Store embedding:")
    print("Store photo:")

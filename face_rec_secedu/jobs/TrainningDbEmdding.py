import os
from deepface import DeepFace
from tqdm import tqdm
 
#pip install redis
import redis
redis = redis.StrictRedis(host='localhost', port=6379, db=0)

for key in redis.scan_iter("embedding:*"):
    redis.delete(key)
    print("Delete embedding:")

for key in redis.scan_iter("photo:*"):
    redis.delete(key)
    print("Delete photo:")

####################### PREPARAÇÃO DO BANCO DE DADOS ######################

#Diretorio de fotos dos cadastros
DIR_DB_IMG = "./workspace/maple"
print("DB Imagens Cadastros: ", DIR_DB_IMG)

#alunos_turma = get_alunos_turma("D0001")
#print("alunos_turma: ", alunos_turma)


# Load the model
models = [
  "VGG-Face", 
  "Facenet", 
  "Facenet512", 
  "OpenFace", 
  "DeepFace", 
  "DeepID", 
  "ArcFace", 
  "Dlib", 
  "SFace",
]

representations = []

for dir_path, dir_name, file_names in os.walk(DIR_DB_IMG):

    for file_name in file_names:
        print("dir_path: ", dir_path)
        print("dir_name: ", dir_name)
        #img_path = os.path.join(dir_path, file_name)
        img_path = f"{dir_path}/{file_name}"
        if img_path.endswith((".png", ".jpg", ".jpeg")):  
            print("img_path: ", img_path)
            embedding_obj = DeepFace.represent(
                img_path=img_path, 
                model_name = models[1], 
                detector_backend='mtcnn',
                enforce_detection=False
                )
            embedding = embedding_obj[0]["embedding"]
            representations.append((img_path, embedding))
        else:
            print("Arquivo inválido ou extensão não suportada.")

#for img_path, embedding in representations:
    #redis_client.rpush(f"embedding:{img_path}", *embedding)

#redis_client.keys()


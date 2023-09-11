from deepface import DeepFace
import os
import time
import redis
from redis.commands.search.field import VectorField, TagField
from redis.commands.search.query import Query
import numpy as np
from tqdm import tqdm
import cv2

DIR_PATH = 'dataset/'
DIR_CAP = 'capturas/'
NAME_MOD = "DeepFace"
BACK_DETECTOT = "opencv"

def represent(img_path, model_name, detector_backend, enforce_detection, align):
    result = {}
    embedding_objs = DeepFace.represent(
        img_path=img_path,
        model_name=model_name,
        detector_backend=detector_backend,
        enforce_detection=enforce_detection,
        align=align,
    )
    result["results"] = embedding_objs
    return result

def verify(
    img1_path, img2_path, model_name, detector_backend, distance_metric, enforce_detection, align
):
    obj = DeepFace.verify(
        img1_path=img1_path,
        img2_path=img2_path,
        model_name=model_name,
        detector_backend=detector_backend,
        distance_metric=distance_metric,
        align=align,
        enforce_detection=enforce_detection,
    )
    return obj

def analyze(img_path, actions, detector_backend, enforce_detection, align):
    result = {}
    demographies = DeepFace.analyze(
        img_path=img_path,
        actions=actions,
        detector_backend=detector_backend,
        enforce_detection=enforce_detection,
        align=align,
    )
    result["results"] = demographies
    return result

def trainning():
    r = redis.Redis( host='secedu-rds-tack', port=6379)
    message =  [ DIR_PATH ]
    name_model = NAME_MOD
    backend_detector = BACK_DETECTOT
    peso , dims = findThreshold(name_model)
    keysDB = r.keys()
    if len(keysDB) > 0:
        embeddings = []
        for dirpath, dirnames, filenames in os.walk(DIR_PATH):
            print(f"Path: {dirpath}")
            for filename in filenames:
                if filename.endswith((".png", ".jpg", ".jpeg")):
                    img_file = f"{dirpath}/{filename}"
                    name = dirpath.split('/')[1].split('/')[0]
                    message.append(name)
                    print(name)
                    embedding = DeepFace.represent(
                        img_path=img_file,
                        model_name=name_model,
                        detector_backend=backend_detector,
                        enforce_detection=False
                        )[0]["embedding"]
                    embeddings.append((name, img_file, embedding))
        
        if len(embeddings) > 0:
            r.flushdb()
            message.append(embeddings)
            pipeline = r.pipeline(transaction=False)
            for person, img_path, embedding in tqdm(embeddings):
                #print(img_path)
                key = img_path.split("/")[-1]
                print(f"FaceID:{person} - EMBEDDING: {embedding} - PATH: {img_path}")
                value = np.array(embedding).astype(np.float32).tobytes()
                # armazenar embedings no redis um a um
                #r.hset(key, mapping = {"embedding": value})

                # armazenar embedings no redis de uma só vez
                #pipeline.hset(key, mapping = {"embedding": value,"name": person})
                pipeline.hset(f"FaceID:{person}", mapping = {"embedding": value, "path": key})

            pipeline_results = pipeline.execute()
            if len(pipeline_results) > 0:
                print('Criando index')
                r.ft().create_index(
                   [
                        VectorField(
                            "embedding",
                            "HNSW",
                            {
                                "TYPE": "FLOAT32",
                                "DIM": dims,
                                "DISTANCE_METRIC": "L2",
                            },
                        )
                    ]
                )
    return message 
             
def findThreshold(model_name):
  threshold = 0
  dims = 128
  if model_name == 'VGG-Face':
    threshold = 0.55
    dims = 2622
  elif model_name == 'OpenFace':
    threshold = 0.55
  elif model_name == 'Facenet':
    threshold = 10
  elif model_name == 'DeepFace':
    threshold = 64
  return [threshold, dims]

def validation(img):
    result = {}
    name_model = NAME_MOD
    backend_detector = BACK_DETECTOT
    peso , dims = findThreshold(name_model)
    target_img = img
    r = redis.Redis( host='secedu-rds-tack', port=6379)
    
    if target_img.endswith((".png", ".jpg", ".jpeg")):

        target_embedding = DeepFace.represent(
            img_path=target_path,
            model_name=name_model,
            detector_backend=backend_detector,
            )[0]["embedding"]

        query_vector = np.array(target_embedding).astype(np.float32).tobytes()

        k = 1
        base_query = f"*=>[KNN {k} @embedding $query_vector AS distance]"
        query = Query(base_query).return_fields("path", "distance").sort_by("distance").dialect(2)
        results = r.ft().search(query, query_params={"query_vector": query_vector})

        for idx, result in enumerate(results.docs):
            id = result.id
            foto = f"{DIR_PATH}/{result.id}/{result.path}"
            distancia = float(result.distance)
            print(
                f"{idx + 1}* vizinho mais próximo é {id} com distância {distancia}"
                )
            if distancia >= peso:
                resultado = DeepFace.verify(target_img,
                                            foto,
                                            model_name=name_model,
                                            detector_backend=backend_detector
                                            )
                print(resultado)
                verify = resultado['verified']
                distancia = resultado['distance']
                thresh = resultado['threshold']

                print(f"Verify: {verify} e distancia: {distancia} / {thresh} x {peso}")
                if verify == True:
                    img2 = cv2.imread(foto)
                    plt.imshow(img2[:, :, ::-1])
                    plt.axis("off")
                    plt.show()

            result["results"] = verify
    return result



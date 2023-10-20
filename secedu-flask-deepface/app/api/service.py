from deepface import DeepFace
import os
import time
import redis
from redis.commands.search.field import VectorField, TagField
from redis.commands.search.query import Query

#Analyze Oval Face
import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import uuid

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

def analyze_mediapipe(img_path, actions, detector_backend='mediapipe', enforce_detection=False, align=True):
    result = []
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)
    img = cv2.imread(img_path)

    results = face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    
    if results.multi_face_landmarks:
        for landmarks in results.multi_face_landmarks:
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
            save_dir = 'media/capturas/ovalFace/'
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            # Gerar um nome de arquivo aleatório
            random_filename = str(uuid.uuid4()) + '.png'
            path = os.path.join(save_dir, random_filename)
            
            # Salvar a imagem no diretório
            cv2.imwrite(path, out)
            print(f"Imagem salva em {path}")
            
            demographies = DeepFace.analyze(
                img_path=path,
                actions=actions,
                detector_backend=detector_backend,
                enforce_detection=enforce_detection,
                align=align,
            )

            result.append({
                "results": demographies,
                "face_location": path
            })
    
    if not result:
        return {"results": "No face detected"}
    
    return result

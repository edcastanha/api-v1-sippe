from flask import Blueprint, request
import cv2
import mediapipe
import pandas as pd
import numpy as np
import os
from deepface import DeepFace

from embedding import Trainning

import service

blueprint = Blueprint("routes", __name__)


@blueprint.route("/")
def home():
    return "<h1>Bem-vindo à SecEdu API!</h1>"

@blueprint.route("/dataset")
def dataset():
    trainning = Trainning()
    trainning.flush_redis()
    keys =  trainning.process_images()
    return keys


@blueprint.route("/represent", methods=["POST"])
def represent():
    input_args = request.get_json()

    if input_args is None:
        return {"message": "conjunto de entrada vazio passado"}

    img_path = input_args.get("img")
    if img_path is None:
        return {"message": "é necessário passar a entrada img_path"}
    
    if img_path.split(".")[-1] not in ["jpg", "png", "jpeg"]:
        return {"message": "é necessário passar a entrada img_path com extensão .jpg, .png ou .jpeg"}
    
    detector_backend = input_args.get("detector_backend", "opencv")
    enforce_detection = input_args.get("enforce_detection", True)
    align = input_args.get("align", True)
    model_name = input_args.get("model_name", "VGG-Face")
    
    try: 
        obj = service.represent(
            img_path=img_path,
            model_name=model_name,
            detector_backend=detector_backend,
            enforce_detection=enforce_detection,
            align=align,
        )
        return obj
    except Exception as e:
        return {"error": str(e)}

@blueprint.route("/verify", methods=["POST"])
def verify():
    input_args = request.get_json()

    if input_args is None:
        return {"message": "empty input set passed"}

    img1_path = input_args.get("img1_path")
    img2_path = input_args.get("img2_path")

    if img1_path is None:
        return {"message": "é necessário passar a entrada imagem_1"}

    if img2_path is None:
        return {"message": "é necessário passar a entrada imagem_2"}

    model_name = input_args.get("model_name", "VGG-Face")
    detector_backend = input_args.get("detector_backend", "opencv")
    enforce_detection = input_args.get("enforce_detection", True)
    distance_metric = input_args.get("distance_metric", "cosine")
    align = input_args.get("align", True)

    verification = service.verify(
        img1_path=img1_path,
        img2_path=img2_path,
        model_name=model_name,
        detector_backend=detector_backend,
        distance_metric=distance_metric,
        align=align,
        enforce_detection=enforce_detection,
    )

    verification["verified"] = str(verification["verified"])

    return verification

@blueprint.route("/analyze", methods=["POST"])
def analyze():
    input_args = request.get_json()
    print(f'Args REQUEST {input_args}')

    if input_args is None:
        return {"message": "conjunto de entrada passado está vazio"}

    img_path = input_args.get("img_path")
    if img_path is None:
        return {"message": "é necessário passar a entrada img_path"}
    
    # Obtém o diretório do arquivo atual (app.py neste caso)
    dir_path = os.path.dirname(os.path.abspath(__file__))

    # Adiciona o nome da pasta que você deseja obter o caminho
    capturas_path = os.path.join( img_path)

    # Verificar se caminho existe ou seria uma imagem (png, jpg ou jpeg)
    if capturas_path is not None and capturas_path.split(".")[-1] not in ["jpg", "png", "jpeg"]:
        return {"message": "é necessário passar a entrada imagem valido com extensão .jpg, .png ou .jpeg"}
    

    detector_backend = input_args.get("detector_backend", "opencv")
    enforce_detection = input_args.get("enforce_detection", True)
    align = input_args.get("align", True)
    actions = input_args.get("actions", ["age", "gender", "emotion", "race"])
    demographies = service.analyze(
        img_path=capturas_path,
        actions=actions,
        detector_backend=detector_backend,
        enforce_detection=enforce_detection,
        align=align,
    )

    # Deletar a imagem após a análise
    #os.remove(capturas_path)

    return demographies

@blueprint.route("/embedding", methods=["POST"])
def embedding():
    input_args = request.get_json()

    if input_args is None:
        return {"message": "conjunto de entrada vazio passado"}

    img_path = input_args.get("img")
    if img_path is None:
        return {"message": "é necessário passar a entrada img_path"}
    
    if img_path.split(".")[-1] not in ["jpg", "png", "jpeg"]:
        return {"message": "é necessário passar a entrada img_path com extensão .jpg, .png ou .jpeg"}
    
    detector_backend = input_args.get("detector_backend", "opencv")
    enforce_detection = input_args.get("enforce_detection", True)
    align = input_args.get("align", True)
    model_name = input_args.get("model_name", "VGG-Face")
    
    
    try: 
        img = cv2.imread(img_path)
        	
        mp_face_mesh = mediapipe.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)

        results = face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        landmarks = results.multi_face_landmarks[0]

        face_oval = mp_face_mesh.FACEMESH_FACE_OVAL
 
        df = pd.DataFrame(list(face_oval), columns = ["p1", "p2"])

        routes_idx = []
        
        p1 = df.iloc[0]["p1"]
        p2 = df.iloc[0]["p2"]
        
        for i in range(0, df.shape[0]):
            
            #print(p1, p2)
            
            obj = df[df["p1"] == p2]
            p1 = obj["p1"].values[0]
            p2 = obj["p2"].values[0]
            
            route_idx = []
            route_idx.append(p1)
            route_idx.append(p2)
            routes_idx.append(route_idx)
        
        
        for route_idx in routes_idx:
            print(f"Traçar uma linha entre o {route_idx[0]}ésimo ponto de referência e o {route_idx[1]}ésimo ponto de referência")

# Extraindo os pontos de referência do rosto
        routes = []
        for source_idx, target_idx in routes_idx:
            
            source = landmarks.landmark[source_idx]
            target = landmarks.landmark[target_idx]
                
            relative_source = (int(img.shape[1] * source.x), int(img.shape[0] * source.y))
            relative_target = (int(img.shape[1] * target.x), int(img.shape[0] * target.y))
        
            #cv2.line(img, relative_source, relative_target, (255, 255, 255), thickness = 2)
            
            routes.append(relative_source)
            routes.append(relative_target)

 
        mask = np.zeros((img.shape[0], img.shape[1]))
        mask = cv2.fillConvexPoly(mask, np.array(routes), 1)
        mask = mask.astype(bool)
        
        out = np.zeros_like(img)
        out[mask] = img[mask]
        
        #fig = plt.figure(figsize = (15, 15))
        #plt.axis('off')
        #plt.imshow(out[:, :, ::-1])

        face = out[:, :, ::-1]
        # -------------------------------

        obj = service.represent(
            img_path=face,
            model_name=model_name,
            detector_backend=detector_backend,
            enforce_detection=enforce_detection,
            align=align,
        )
        return obj
    except Exception as e:
        return {"error": str(e)}
    
@blueprint.route("/mediapipe", methods=["POST"])
def analanalyze_mediapipe():
    input_args = request.get_json()
    print(f'Args REQUEST {input_args}')

    if input_args is None:
        return {"message": "conjunto de entrada passado está vazio"}

    img_path = input_args.get("img_path")
    if img_path is None:
        return {"message": "é necessário passar a entrada img_path"}
    
    # Obtém o diretório do arquivo atual (app.py neste caso)
    dir_path = os.path.dirname(os.path.abspath(__file__))

    # Adiciona o nome da pasta que você deseja obter o caminho
    capturas_path = os.path.join( img_path)

    # Verificar se caminho existe ou seria uma imagem (png, jpg ou jpeg)
    if capturas_path is not None and capturas_path.split(".")[-1] not in ["jpg", "png", "jpeg"]:
        return {"message": "é necessário passar a entrada imagem valido com extensão .jpg, .png ou .jpeg"}
    
    faces = DeepFace.build_model()
    
    detector_backend = input_args.get("detector_backend", "opencv")
    enforce_detection = input_args.get("enforce_detection", True)
    align = input_args.get("align", True)
    actions = input_args.get("actions", ["age", "gender", "emotion", "race"])
    demographies = service.analyze_mediapipe(
        img_path=capturas_path,
        actions=actions,
        detector_backend=detector_backend,
        enforce_detection=enforce_detection,
        align=align,
    )

    # Deletar a imagem após a análise
    #os.remove(capturas_path)

    return demographies


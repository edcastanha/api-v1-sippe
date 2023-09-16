# common dependencies
import os
from os import path
import warnings
import time
import pickle
import logging

# 3rd party dependencies
import numpy as np
import pandas as pd
from tqdm import tqdm
import cv2
import tensorflow as tf
from deprecated import deprecated

# package dependencies
from deepface.basemodels import (
    VGGFace,
    OpenFace,
    Facenet,
    Facenet512,
    FbDeepFace,
    DeepID,
    DlibWrapper,
    ArcFace,
    SFace,
)
from deepface.extendedmodels import Age, Gender, Race, Emotion
from deepface.commons import functions, realtime, distance as dst

# -----------------------------------
# configurations for dependencies

warnings.filterwarnings("ignore")
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
tf_version = int(tf.__version__.split(".", maxsplit=1)[0])
if tf_version == 2:
    tf.get_logger().setLevel(logging.ERROR)
# -----------------------------------


def build_model(model_name):
    """
    Esta função cria um modelo de superfície profunda
    Parâmetros:
            model_name (string): modelo de reconhecimento facial ou de atributos faciais
                    VGG-Face, Facenet, OpenFace, DeepFace, DeepID para reconhecimento facial
                    Idade, Género, Emoção, Raça para atributos faciais

    Retorna:
            modelo deepface construído
    """

    # singleton design pattern
    global model_obj

    models = {
        "VGG-Face": VGGFace.loadModel,
        "OpenFace": OpenFace.loadModel,
        "Facenet": Facenet.loadModel,
        "Facenet512": Facenet512.loadModel,
        "DeepFace": FbDeepFace.loadModel,
        "DeepID": DeepID.loadModel,
        "Dlib": DlibWrapper.loadModel,
        "ArcFace": ArcFace.loadModel,
        "SFace": SFace.load_model,
        "Emotion": Emotion.loadModel,
        "Age": Age.loadModel,
        "Gender": Gender.loadModel,
        "Race": Race.loadModel,
    }

    if not "model_obj" in globals():
        model_obj = {}

    if not model_name in model_obj:
        model = models.get(model_name)
        if model:
            model = model()
            model_obj[model_name] = model
        else:
            raise ValueError(f"Invalid model_name passed - {model_name}")

    return model_obj[model_name]


def verify(
    img1_path,
    img2_path,
    model_name="VGG-Face",
    detector_backend="opencv",
    distance_metric="cosine",
    enforce_detection=True,
    align=True,
    normalization="base",
):
    """
    Esta função verifica se um par de imagens é a mesma pessoa ou pessoas diferentes. Em segundo plano,
    função de verificação representa as imagens faciais como vectores e depois calcula a semelhança
    entre esses vectores. Os vectores das imagens da mesma pessoa devem ter mais semelhança (ou menos
    distância) do que os vectores de pessoas diferentes.

    Parâmetros:
            img1_path, img2_path: caminho exato da imagem como string. array numpy (BGR) ou imagens codificadas em based64
            também são bem-vindas. Se um dos pares tiver mais do que uma face, então comparamos o par de faces
            par de faces com similaridade máxima.

            nome_do_modelo (str): VGG-Face, Facenet, Facenet512, OpenFace, DeepFace, DeepID, Dlib
            ArcFace e SFace

            distance_metric (string): cosine, euclidean, euclidean_l2

            enforce_detection (booleano): Se não for possível detetar nenhuma face numa imagem, então esta
            função devolverá uma exceção por defeito. Defina este valor como False para não ter esta exceção.
            Isto pode ser conveniente para imagens de baixa resolução.

            detector_backend (string): define o backend do detetor de faces para opencv, retinaface, mtcnn, ssd,
            dlib, mediapipe ou yolov8.

            align (boolean): alinhamento de acordo com as posições dos olhos.

            normalization (string): normaliza a imagem de entrada antes de alimentar o modelo

    Retorna:
            A função Verify devolve um dicionário.

            {
                    "verified" (verificado): True
                    , "distância": 0.2563
                    , "max_threshold_to_verify": 0.40
                    , "modelo": "VGG-Face"
                    , "similarity_metric": "cosine"
                    , "facial_areas": {
                            'img1': {'x': 345, 'y': 211, 'w': 769, 'h': 769},
                            'img2': {'x': 318, 'y': 534, 'w': 779, 'h': 779}
                    }
                    , "time": 2
            }

    """

    tic = time.time()

    # --------------------------------
    target_size = functions.find_target_size(model_name=model_name)

    # img pairs might have many faces
    img1_objs = functions.extract_faces(
        img=img1_path,
        target_size=target_size,
        detector_backend=detector_backend,
        grayscale=False,
        enforce_detection=enforce_detection,
        align=align,
    )

    img2_objs = functions.extract_faces(
        img=img2_path,
        target_size=target_size,
        detector_backend=detector_backend,
        grayscale=False,
        enforce_detection=enforce_detection,
        align=align,
    )
    # --------------------------------
    distances = []
    regions = []
    # now we will find the face pair with minimum distance
    for img1_content, img1_region, _ in img1_objs:
        for img2_content, img2_region, _ in img2_objs:
            img1_embedding_obj = represent(
                img_path=img1_content,
                model_name=model_name,
                enforce_detection=enforce_detection,
                detector_backend="skip",
                align=align,
                normalization=normalization,
            )

            img2_embedding_obj = represent(
                img_path=img2_content,
                model_name=model_name,
                enforce_detection=enforce_detection,
                detector_backend="skip",
                align=align,
                normalization=normalization,
            )

            img1_representation = img1_embedding_obj[0]["embedding"]
            img2_representation = img2_embedding_obj[0]["embedding"]

            if distance_metric == "cosine":
                distance = dst.findCosineDistance(img1_representation, img2_representation)
            elif distance_metric == "euclidean":
                distance = dst.findEuclideanDistance(img1_representation, img2_representation)
            elif distance_metric == "euclidean_l2":
                distance = dst.findEuclideanDistance(
                    dst.l2_normalize(img1_representation), dst.l2_normalize(img2_representation)
                )
            else:
                raise ValueError("Invalid distance_metric passed - ", distance_metric)

            distances.append(distance)
            regions.append((img1_region, img2_region))

    # -------------------------------
    threshold = dst.findThreshold(model_name, distance_metric)
    distance = min(distances)  # best distance
    facial_areas = regions[np.argmin(distances)]

    toc = time.time()

    resp_obj = {
        "verified": distance <= threshold,
        "distance": distance,
        "threshold": threshold,
        "model": model_name,
        "detector_backend": detector_backend,
        "similarity_metric": distance_metric,
        "facial_areas": {"img1": facial_areas[0], "img2": facial_areas[1]},
        "time": round(toc - tic, 2),
    }

    return resp_obj


def analyze(
    img_path,
    actions=("emotion", "age", "gender", "race"),
    enforce_detection=True,
    detector_backend="opencv",
    align=True,
    silent=False,
):
    """
    Esta função analisa os atributos faciais, incluindo a idade, o sexo, a emoção e a raça.
    Em segundo plano, a função de análise constrói modelos de rede neural convolucional para
    classificar a idade, o género, a emoção e a raça da imagem de entrada.

    Parâmetros:
            img_path: pode ser passado o caminho exato da imagem, uma matriz numpy (BGR) ou uma imagem codificada em base64.
            Se a imagem de origem tiver mais de um rosto, o resultado será o tamanho do número de rostos
            que aparecem na imagem.

            acções (tupla): A predefinição é ('idade', 'género', 'emoção', 'raça'). Pode eliminar
            alguns desses atributos.

            enforce_detection (bool): A função lança uma exceção se nenhum rosto for detectado por defeito.
            Defina isto para False se não quiser receber uma exceção. Isto pode ser conveniente para imagens de baixa
            baixa resolução.

            detector_backend (string): define o backend do detetor de faces para opencv, retinaface, mtcnn, ssd,
            dlib, mediapipe ou yolov8.

            align (booleano): alinhamento de acordo com as posições dos olhos.

            silent (boolean): desativar (algumas) mensagens de registo

    Retorna:
            A função retorna uma lista de dicionários para cada rosto que aparece na imagem.

            [
                    {
                            "region": {'x': 230, 'y': 120, 'w': 36, 'h': 45},
                            "idade": 28.66,
                            "género_dominante": "Mulher",
                            "género": {
                                    'Mulher': 99.99407529830933,
                                    'Homem': 0.005928758764639497,
                            }
                            "dominant_emotion" (emoção dominante): "neutral",
                            "emotion" (emoção): {
                                    'triste': 37.65260875225067,
                                    'zangado': 0.15512987738475204,
                                    'surprise': 0.0022171278033056296,
                                    'medo': 1.2489334680140018,
                                    'feliz': 4.609785228967667,
                                    'disgust': 9.698561953541684e-07,
                                    'neutral': 56.33133053779602
                            }
                            "dominant_race": "branco",
                            "race": {
                                    'indiano': 0.5480832420289516,
                                    'asian': 0.7830780930817127,
                                    'latino hispânico': 2.0677512511610985,
                                    'black': 0.06337375962175429,
                                    'middle eastern': 3.088453598320484,
                                    'white' (branco): 93.44925880432129
                            }
                    }
            ]

    """
    # ---------------------------------
    # validate actions
    if isinstance(actions, str):
        actions = (actions,)

    # check if actions is not an iterable or empty.
    if not hasattr(actions, "__getitem__") or not actions:
        raise ValueError("`actions` must be a list of strings.")

    actions = list(actions)

    # For each action, check if it is valid
    for action in actions:
        if action not in ("emotion", "age", "gender", "race"):
            raise ValueError(
                f"Invalid action passed ({repr(action)})). "
                "Valid actions are `emotion`, `age`, `gender`, `race`."
            )
    # ---------------------------------
    # build models
    models = {}
    if "emotion" in actions:
        models["emotion"] = build_model("Emotion")

    if "age" in actions:
        models["age"] = build_model("Age")

    if "gender" in actions:
        models["gender"] = build_model("Gender")

    if "race" in actions:
        models["race"] = build_model("Race")
    # ---------------------------------
    resp_objects = []

    img_objs = functions.extract_faces(
        img=img_path,
        target_size=(224, 224),
        detector_backend=detector_backend,
        grayscale=False,
        enforce_detection=enforce_detection,
        align=align,
    )

    for img_content, img_region, _ in img_objs:
        if img_content.shape[0] > 0 and img_content.shape[1] > 0:
            obj = {}
            # facial attribute analysis
            pbar = tqdm(range(0, len(actions)), desc="Finding actions", disable=silent)
            for index in pbar:
                action = actions[index]
                pbar.set_description(f"Action: {action}")

                if action == "emotion":
                    img_gray = cv2.cvtColor(img_content[0], cv2.COLOR_BGR2GRAY)
                    img_gray = cv2.resize(img_gray, (48, 48))
                    img_gray = np.expand_dims(img_gray, axis=0)

                    emotion_predictions = models["emotion"].predict(img_gray, verbose=0)[0, :]

                    sum_of_predictions = emotion_predictions.sum()

                    obj["emotion"] = {}

                    for i, emotion_label in enumerate(Emotion.labels):
                        emotion_prediction = 100 * emotion_predictions[i] / sum_of_predictions
                        obj["emotion"][emotion_label] = emotion_prediction

                    obj["dominant_emotion"] = Emotion.labels[np.argmax(emotion_predictions)]

                elif action == "age":
                    age_predictions = models["age"].predict(img_content, verbose=0)[0, :]
                    apparent_age = Age.findApparentAge(age_predictions)
                    # int cast is for exception - object of type 'float32' is not JSON serializable
                    obj["age"] = int(apparent_age)

                elif action == "gender":
                    gender_predictions = models["gender"].predict(img_content, verbose=0)[0, :]
                    obj["gender"] = {}
                    for i, gender_label in enumerate(Gender.labels):
                        gender_prediction = 100 * gender_predictions[i]
                        obj["gender"][gender_label] = gender_prediction

                    obj["dominant_gender"] = Gender.labels[np.argmax(gender_predictions)]

                elif action == "race":
                    race_predictions = models["race"].predict(img_content, verbose=0)[0, :]
                    sum_of_predictions = race_predictions.sum()

                    obj["race"] = {}
                    for i, race_label in enumerate(Race.labels):
                        race_prediction = 100 * race_predictions[i] / sum_of_predictions
                        obj["race"][race_label] = race_prediction

                    obj["dominant_race"] = Race.labels[np.argmax(race_predictions)]

                # -----------------------------
                # mention facial areas
                obj["region"] = img_region

            resp_objects.append(obj)

    return resp_objects


def find(
    img_path,
    db_path,
    model_name="VGG-Face",
    distance_metric="cosine",
    enforce_detection=True,
    detector_backend="opencv",
    align=True,
    normalization="base",
    silent=False,
):
    """
    Esta função aplica a verificação várias vezes e encontra as identidades numa base de dados

    Parâmetros:
            img_path: caminho exato da imagem, matriz numpy (BGR) ou imagem codificada com base64.
            A imagem de origem pode ter muitas faces. Então, o resultado será o tamanho do número de
            faces na imagem de origem.

            db_path (string): Você deve armazenar alguns arquivos de imagem numa pasta e passar o
            caminho exato para esta pasta. Uma imagem da base de dados também pode ter muitas faces.
            Então, todas as faces detectadas na base de dados serão consideradas na decisão.

            nome_do_modelo (string): VGG-Face, Facenet, Facenet512, OpenFace, DeepFace, DeepID,
            Dlib, ArcFace, SFace ou Ensemble

            distance_metric (string): cosseno, euclideano, euclidean_l2

            enforce_detection (bool): A função lança uma exceção se não for possível detetar uma face.
            Defina isto como False se não quiser obter uma exceção. Isto pode ser conveniente para imagens de baixa
            baixa resolução.

            detector_backend (string): define o backend do detetor de faces para opencv, retinaface, mtcnn, ssd,
            dlib, mediapipe ou yolov8.

            align (boolean): alinhamento de acordo com as posições dos olhos.

            normalization (string): normaliza a imagem de entrada antes de alimentar o modelo

            silent (boolean): desativar alguns registos e barras de progresso

    Retorna:
            Esta função devolve uma lista de quadros de dados pandas. Cada item da lista corresponde a
            uma identidade no caminho_img.
    """

    tic = time.time()

    # -------------------------------
    if os.path.isdir(db_path) is not True:
        raise ValueError("Passed db_path does not exist!")

    target_size = functions.find_target_size(model_name=model_name)

    # ---------------------------------------

    file_name = f"representations_{model_name}.pkl"
    file_name = file_name.replace("-", "_").lower()

    if path.exists(db_path + "/" + file_name):

        if not silent:
            print(
                f"WARNING: Representations for images in {db_path} folder were previously stored"
                + f" in {file_name}. If you added new instances after the creation, then please "
                + "delete this file and call find function again. It will create it again."
            )

        with open(f"{db_path}/{file_name}", "rb") as f:
            representations = pickle.load(f)

        if not silent:
            print("There are ", len(representations), " representations found in ", file_name)

    else:  # create representation.pkl from scratch
        employees = []

        for r, _, f in os.walk(db_path):
            for file in f:
                if (
                    (".jpg" in file.lower())
                    or (".jpeg" in file.lower())
                    or (".png" in file.lower())
                ):
                    exact_path = r + "/" + file
                    employees.append(exact_path)

        if len(employees) == 0:
            raise ValueError(
                "There is no image in ",
                db_path,
                " folder! Validate .jpg or .png files exist in this path.",
            )

        # ------------------------
        # find representations for db images

        representations = []

        # for employee in employees:
        pbar = tqdm(
            range(0, len(employees)),
            desc="Finding representations",
            disable=silent,
        )
        for index in pbar:
            employee = employees[index]

            img_objs = functions.extract_faces(
                img=employee,
                target_size=target_size,
                detector_backend=detector_backend,
                grayscale=False,
                enforce_detection=enforce_detection,
                align=align,
            )

            for img_content, _, _ in img_objs:
                embedding_obj = represent(
                    img_path=img_content,
                    model_name=model_name,
                    enforce_detection=enforce_detection,
                    detector_backend="skip",
                    align=align,
                    normalization=normalization,
                )

                img_representation = embedding_obj[0]["embedding"]

                instance = []
                instance.append(employee)
                instance.append(img_representation)
                representations.append(instance)

        # -------------------------------

        with open(f"{db_path}/{file_name}", "wb") as f:
            pickle.dump(representations, f)

        if not silent:
            print(
                f"Representations stored in {db_path}/{file_name} file."
                + "Please delete this file when you add new identities in your database."
            )

    # ----------------------------
    # now, we got representations for facial database
    df = pd.DataFrame(representations, columns=["identity", f"{model_name}_representation"])

    # img path might have more than once face
    target_objs = functions.extract_faces(
        img=img_path,
        target_size=target_size,
        detector_backend=detector_backend,
        grayscale=False,
        enforce_detection=enforce_detection,
        align=align,
    )

    resp_obj = []

    for target_img, target_region, _ in target_objs:
        target_embedding_obj = represent(
            img_path=target_img,
            model_name=model_name,
            enforce_detection=enforce_detection,
            detector_backend="skip",
            align=align,
            normalization=normalization,
        )

        target_representation = target_embedding_obj[0]["embedding"]

        result_df = df.copy()  # df will be filtered in each img
        result_df["source_x"] = target_region["x"]
        result_df["source_y"] = target_region["y"]
        result_df["source_w"] = target_region["w"]
        result_df["source_h"] = target_region["h"]

        distances = []
        for index, instance in df.iterrows():
            source_representation = instance[f"{model_name}_representation"]

            if distance_metric == "cosine":
                distance = dst.findCosineDistance(source_representation, target_representation)
            elif distance_metric == "euclidean":
                distance = dst.findEuclideanDistance(source_representation, target_representation)
            elif distance_metric == "euclidean_l2":
                distance = dst.findEuclideanDistance(
                    dst.l2_normalize(source_representation),
                    dst.l2_normalize(target_representation),
                )
            else:
                raise ValueError(f"invalid distance metric passes - {distance_metric}")

            distances.append(distance)

            # ---------------------------

        result_df[f"{model_name}_{distance_metric}"] = distances

        threshold = dst.findThreshold(model_name, distance_metric)
        result_df = result_df.drop(columns=[f"{model_name}_representation"])
        result_df = result_df[result_df[f"{model_name}_{distance_metric}"] <= threshold]
        result_df = result_df.sort_values(
            by=[f"{model_name}_{distance_metric}"], ascending=True
        ).reset_index(drop=True)

        resp_obj.append(result_df)

    # -----------------------------------

    toc = time.time()

    if not silent:
        print("find function lasts ", toc - tic, " seconds")

    return resp_obj


def represent(
    img_path,
    model_name="VGG-Face",
    enforce_detection=True,
    detector_backend="opencv",
    align=True,
    normalization="base",
):
    """
    Esta função representa imagens faciais como vectores. A função utiliza modelos de redes neurais convolucionais
    neurais convolucionais para gerar a incorporação de vectores.

    Parâmetros:
            img_path (string): caminho exato da imagem. Em alternativa, pode ser passada uma matriz numpy (BGR) ou imagens codificadas em based64
            podem ser passadas imagens codificadas. A imagem de origem pode ter muitas faces. Então, o resultado será
            será o tamanho do número de faces que aparecem na imagem de origem.

            nome_do_modelo (string): VGG-Face, Facenet, Facenet512, OpenFace, DeepFace, DeepID, Dlib,
            ArcFace, SFace

            enforce_detection (booleano): Se não for possível detetar nenhuma face numa imagem, esta
            função devolverá uma exceção por defeito. Defina este valor como False para não ter esta exceção.
            Isto pode ser conveniente para imagens de baixa resolução.

            detector_backend (string): define o backend do detetor de faces para opencv, retinaface, mtcnn, ssd,
            dlib, mediapipe ou yolov8.

            align (boolean): alinhamento de acordo com as posições dos olhos.

            normalization (string): normaliza a imagem de entrada antes de alimentar o modelo

    Retorna:
            A função de representação devolve uma lista de objectos com um vetor multidimensional (embedding).
            O número de dimensões está a mudar com base no modelo de referência.
            Por exemplo, FaceNet devolve um vetor de 128 dimensões; VGG-Face devolve um vetor de 2622 dimensões.
    """
    resp_objs = []

    model = build_model(model_name)

    # ---------------------------------
    # we have run pre-process in verification. so, this can be skipped if it is coming from verify.
    target_size = functions.find_target_size(model_name=model_name)
    if detector_backend != "skip":
        img_objs = functions.extract_faces(
            img=img_path,
            target_size=target_size,
            detector_backend=detector_backend,
            grayscale=False,
            enforce_detection=enforce_detection,
            align=align,
        )
    else:  # skip
        if isinstance(img_path, str):
            img = functions.load_image(img_path)
        elif type(img_path).__module__ == np.__name__:
            img = img_path.copy()
        else:
            raise ValueError(f"unexpected type for img_path - {type(img_path)}")
        # --------------------------------
        if len(img.shape) == 4:
            img = img[0]  # e.g. (1, 224, 224, 3) to (224, 224, 3)
        if len(img.shape) == 3:
            img = cv2.resize(img, target_size)
            img = np.expand_dims(img, axis=0)
        # --------------------------------
        img_region = [0, 0, img.shape[1], img.shape[0]]
        img_objs = [(img, img_region, 0)]
    # ---------------------------------

    for img, region, confidence in img_objs:
        # custom normalization
        img = functions.normalize_input(img=img, normalization=normalization)

        # represent
        if "keras" in str(type(model)):
            # new tf versions show progress bar and it is annoying
            embedding = model.predict(img, verbose=0)[0].tolist()
        else:
            # SFace and Dlib are not keras models and no verbose arguments
            embedding = model.predict(img)[0].tolist()

        resp_obj = {}
        resp_obj["embedding"] = embedding
        resp_obj["facial_area"] = region
        resp_obj["face_confidence"] = confidence
        resp_objs.append(resp_obj)

    return resp_objs


def stream(
    db_path="",
    model_name="VGG-Face",
    detector_backend="opencv",
    distance_metric="cosine",
    enable_face_analysis=True,
    source=0,
    time_threshold=5,
    frame_threshold=5,
):
    """
    Esta função aplica o reconhecimento facial em tempo real e a análise dos atributos faciais

    Parâmetros:
            db_path (string): caminho da base de dados facial. Deve guardar alguns ficheiros .jpg nesta pasta.

            model_name (string): VGG-Face, Facenet, Facenet512, OpenFace, DeepFace, DeepID, Dlib,
            ArcFace, SFace

            detector_backend (string): opencv, retinaface, mtcnn, ssd, dlib, mediapipe ou yolov8.

            distance_metric (string): cosine, euclidean, euclidean_l2

            enable_facial_analysis (boolean): Defina como False para executar apenas o reconhecimento facial

            source (fonte): Defina este valor como 0 para aceder à câmara Web. Caso contrário, passe o caminho exato do vídeo.

            time_threshold (int): quantos segundos a imagem analisada será apresentada

            frame_threshold (int): quantos frames são necessários para focar a face

    """

    if time_threshold < 1:
        raise ValueError(
            "time_threshold must be greater than the value 1 but you passed " + str(time_threshold)
        )

    if frame_threshold < 1:
        raise ValueError(
            "frame_threshold must be greater than the value 1 but you passed "
            + str(frame_threshold)
        )

    realtime.analysis(
        db_path,
        model_name,
        detector_backend,
        distance_metric,
        enable_face_analysis,
        source=source,
        time_threshold=time_threshold,
        frame_threshold=frame_threshold,
    )


def extract_faces(
    img_path,
    target_size=(224, 224),
    detector_backend="opencv",
    enforce_detection=True,
    align=True,
    grayscale=False,
):
    """
    Esta função aplica as fases de pré-processamento de um pipeline de reconhecimento facial
    incluindo deteção e alinhamento

    Parameters:
            img_path: caminho exato da imagem, matriz numpy (BGR) ou imagem codificada em base64.
            A imagem de origem pode ter muitas faces. Então, o resultado será o tamanho do número
            de faces que aparecem nessa imagem de origem.

            target_size (tupla): forma final da imagem facial. Os pixéis pretos serão
            adicionados para redimensionar a imagem.

            detector_backend (string): os backends de deteção facial são retinaface, mtcnn,
            opencv, ssd ou dlib

            enforce_detection (boolean): a função lança uma exceção se a face não puder ser
            detectada na imagem alimentada. Defina este valor como False se não pretender obter
            uma exceção e executar a função na mesma.

            align (booleano): alinhamento de acordo com as posições dos olhos.

            grayscale (booleano): extração de faces em rgb ou escala de cinzentos

    Returns:
            lista de dicionários. Cada dicionário terá a própria imagem facial,
            a área extraída da imagem original e a pontuação de confiança.

    """

    resp_objs = []
    img_objs = functions.extract_faces(
        img=img_path,
        target_size=target_size,
        detector_backend=detector_backend,
        grayscale=grayscale,
        enforce_detection=enforce_detection,
        align=align,
    )

    for img, region, confidence in img_objs:
        resp_obj = {}

        # discard expanded dimension
        if len(img.shape) == 4:
            img = img[0]

        resp_obj["face"] = img[:, :, ::-1]
        resp_obj["facial_area"] = region
        resp_obj["confidence"] = confidence
        resp_objs.append(resp_obj)

    return resp_objs


# ---------------------------
# deprecated functions


@deprecated(version="0.0.78", reason="Use DeepFace.extract_faces instead of DeepFace.detectFace")
def detectFace(
    img_path, target_size=(224, 224), detector_backend="opencv", enforce_detection=True, align=True
):
    """
    Deprecated function. Use extract_faces for same functionality.

    This function applies pre-processing stages of a face recognition pipeline
    including detection and alignment

    Parameters:
            img_path: exact image path, numpy array (BGR) or base64 encoded image.
            Source image can have many face. Then, result will be the size of number
            of faces appearing in that source image.

            target_size (tuple): final shape of facial image. black pixels will be
            added to resize the image.

            detector_backend (string): face detection backends are retinaface, mtcnn,
            opencv, ssd or dlib

            enforce_detection (boolean): function throws exception if face cannot be
            detected in the fed image. Set this to False if you do not want to get
            an exception and run the function anyway.

            align (boolean): alignment according to the eye positions.

            grayscale (boolean): extracting faces in rgb or gray scale

    Returns:
            detected and aligned face as numpy array

    """
    print("⚠️ Function detectFace is deprecated. Use extract_faces instead.")
    face_objs = extract_faces(
        img_path=img_path,
        target_size=target_size,
        detector_backend=detector_backend,
        enforce_detection=enforce_detection,
        align=align,
        grayscale=False,
    )

    extracted_face = None
    if len(face_objs) > 0:
        extracted_face = face_objs[0]["face"]
    return extracted_face


# ---------------------------
# main

functions.initialize_folder()


def cli():
    """
    command line interface function will be offered in this block
    """
    import fire

    fire.Fire()

import os
import base64
from pathlib import Path
from PIL import Image
import requests

# 3rd party dependencies
import numpy as np
import cv2
import tensorflow as tf
from deprecated import deprecated

# package dependencies
from deepface.detectors import FaceDetector


# --------------------------------------------------
# configurations of dependencies

tf_version = tf.__version__
tf_major_version = int(tf_version.split(".", maxsplit=1)[0])
tf_minor_version = int(tf_version.split(".")[1])

if tf_major_version == 1:
    from keras.preprocessing import image
elif tf_major_version == 2:
    from tensorflow.keras.preprocessing import image

# --------------------------------------------------


def initialize_folder():
    """Initialize the folder for storing weights and models.

    Raises:
        OSError: if the folder cannot be created.
    """
    home = get_deepface_home()
    deepFaceHomePath = home + "/.deepface"
    weightsPath = deepFaceHomePath + "/weights"

    if not os.path.exists(deepFaceHomePath):
        os.makedirs(deepFaceHomePath, exist_ok=True)
        print("Directory ", home, "/.deepface created")

    if not os.path.exists(weightsPath):
        os.makedirs(weightsPath, exist_ok=True)
        print("Directory ", home, "/.deepface/weights created")


def get_deepface_home():
    """Get the home directory for storing weights and models.

    Returns:
        str: the home directory.
    """
    return str(os.getenv("DEEPFACE_HOME", default=str(Path.home())))


# --------------------------------------------------


def loadBase64Img(uri):
    """Load image from base64 string.

    Args:
        uri: a base64 string.

    Returns:
        numpy array: the loaded image.
    """
    encoded_data = uri.split(",")[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def load_image(img):
    """Load image from path, url, base64 or numpy array.

    Args:
        img: a path, url, base64 or numpy array.

    Raises:
        ValueError: if the image path does not exist.

    Returns:
        numpy array: the loaded image.
    """
    # The image is already a numpy array
    if type(img).__module__ == np.__name__:
        return img

    # The image is a base64 string
    if img.startswith("data:image/"):
        return loadBase64Img(img)

    # The image is a url
    if img.startswith("http"):
        return np.array(Image.open(requests.get(img, stream=True, timeout=60).raw).convert("RGB"))[
            :, :, ::-1
        ]

    # The image is a path
    if os.path.isfile(img) is not True:
        raise ValueError(f"Confirm that {img} exists")

    # For reading images with unicode names
    with open(img, "rb") as img_f:
        chunk = img_f.read()
        chunk_arr = np.frombuffer(chunk, dtype=np.uint8)
        img = cv2.imdecode(chunk_arr, cv2.IMREAD_COLOR)
    return img

    # This causes troubles when reading files with non english names
    # return cv2.imread(img)

# --------------------------------------------------


def extract_faces(
    img,
    target_size=(224, 224),
    detector_backend="opencv",
    grayscale=False,
    enforce_detection=True,
    align=True,
):
    """Extract faces from an image.

    Args:
        img: um caminho, url, base64 ou array numpy.
        target_size (tupla, opcional): o tamanho alvo das faces extraídas.
        O padrão é (224, 224).
        detector_backend (str, opcional): o backend do detetor de faces. A predefinição é "opencv".
        grayscale (bool, opcional): se as faces extraídas devem ser convertidas em escala de cinzentos.
        A predefinição é False.
        enforce_detection (bool, opcional): se deve ser aplicada a deteção de rostos. A predefinição é Verdadeiro.
        align (bool, opcional): se deve alinhar as faces extraídas. A predefinição é Verdadeiro.

    Levanta:
        ValueError: se a face não puder ser detectada e enforce_detection for True.

    Retorna:
        list: uma lista de faces extraídas.
    """

    # this is going to store a list of img itself (numpy), it region and confidence
    extracted_faces = []

    # img might be path, base64 or numpy array. Convert it to numpy whatever it is.
    img = load_image(img)
    img_region = [0, 0, img.shape[1], img.shape[0]]

    if detector_backend == "skip":
        face_objs = [(img, img_region, 0)]
    else:
        face_detector = FaceDetector.build_model(detector_backend)
        face_objs = FaceDetector.detect_faces(face_detector, detector_backend, img, align)

    # in case of no face found
    if len(face_objs) == 0 and enforce_detection is True:
        raise ValueError(
            "Não foi possível detetar o rosto. Confirme se a imagem é uma fotografia de rosto "
            + "ou considerar a possibilidade de definir o parâmetro enforce_detection como False."
        )

    if len(face_objs) == 0 and enforce_detection is False:
        face_objs = [(img, img_region, 0)]

    for current_img, current_region, confidence in face_objs:
        if current_img.shape[0] > 0 and current_img.shape[1] > 0:
            if grayscale is True:
                current_img = cv2.cvtColor(current_img, cv2.COLOR_BGR2GRAY)

            # resize and padding
            if current_img.shape[0] > 0 and current_img.shape[1] > 0:
                factor_0 = target_size[0] / current_img.shape[0]
                factor_1 = target_size[1] / current_img.shape[1]
                factor = min(factor_0, factor_1)

                dsize = (
                    int(current_img.shape[1] * factor),
                    int(current_img.shape[0] * factor),
                )
                current_img = cv2.resize(current_img, dsize)

                diff_0 = target_size[0] - current_img.shape[0]
                diff_1 = target_size[1] - current_img.shape[1]
                if grayscale is False:
                    # Colocar a imagem de base no meio da imagem almofadada
                    current_img = np.pad(
                        current_img,
                        (
                            (diff_0 // 2, diff_0 - diff_0 // 2),
                            (diff_1 // 2, diff_1 - diff_1 // 2),
                            (0, 0),
                        ),
                        "constant",
                    )
                else:
                    current_img = np.pad(
                        current_img,
                        (
                            (diff_0 // 2, diff_0 - diff_0 // 2),
                            (diff_1 // 2, diff_1 - diff_1 // 2),
                        ),
                        "constant",
                    )

            # verificação dupla: se a imagem de destino não tiver ainda o mesmo tamanho que a imagem de destino.
            if current_img.shape[0:2] != target_size:
                current_img = cv2.resize(current_img, target_size)

            # normalizar os pixéis da imagem
            # o que é que esta linha faz? deve?
            img_pixels = image.img_to_array(current_img)
            img_pixels = np.expand_dims(img_pixels, axis=0)
            img_pixels /= 255  # normalize input in [0, 1]

            # O int cast é para a exceção - o objeto do tipo 'float32' não é serializável em JSON
            region_obj = {
                "x": int(current_region[0]),
                "y": int(current_region[1]),
                "w": int(current_region[2]),
                "h": int(current_region[3]),
            }

            extracted_face = [img_pixels, region_obj, confidence]
            extracted_faces.append(extracted_face)

    if len(extracted_faces) == 0 and enforce_detection == True:
        raise ValueError(
            f"Detected face shape is {img.shape}. Consider to set enforce_detection arg to False."
        )

    return extracted_faces


def normalize_input(img, normalization="base"):
    """Normalize input image.

    Args:
        img (numpy array): a imagem de entrada.
        normalization (str, opcional): a técnica de normalização. O padrão é "base",
        para nenhuma normalização.

    Returns:
        numpy array: the normalized image.
    """

    # A questão 131 declara que algumas técnicas de normalização melhoram a exatidão

    if normalization == "base":
        return img

    # @trevorgribble e @davedgd contribuíram com esta funcionalidade
    # restaurar a entrada na escala de [0, 255] porque foi normalizada na escala de
    # [0, 1] em preprocess_face
    img *= 255

    if normalization == "raw":
        pass  # devolver apenas os pixéis restaurados

    elif normalization == "Facenet":
        mean, std = img.mean(), img.std()
        img = (img - mean) / std

    elif normalization == "Facenet2018":
        # simply / 127.5 - 1 (semelhante ao passo de pré-processamento do modelo facenet 2018, tal como @iamrishab publicou)
        img /= 127.5
        img -= 1

    elif normalization == "VGGFace":
        # subtração média baseada nos dados de treino VGGFace1
        img[..., 0] -= 93.5940
        img[..., 1] -= 104.7624
        img[..., 2] -= 129.1863

    elif normalization == "VGGFace2":
        # subtração média baseada em dados de treino VGGFace2
        img[..., 0] -= 91.4953
        img[..., 1] -= 103.8827
        img[..., 2] -= 131.0912

    elif normalization == "ArcFace":
        # Estudo de referência: Os rostos são cortados e redimensionados para 112×112,
        # e cada pixel (variando entre [0, 255]) nas imagens RGB é normalizado
        # subtraindo 127,5 e dividindo por 128.
        img -= 127.5
        img /= 128
    else:
        raise ValueError(f"tipo de normalização não implementado - {normalization}")

    return img


def find_target_size(model_name):
    """Encontra o tamanho alvo do modelo.

    Args:
        nome_do_modelo (str): o nome do modelo.

    Retorna:
        tuple: o tamanho alvo.
    """

    target_sizes = {
        "VGG-Face": (224, 224),
        "Facenet": (160, 160),
        "Facenet512": (160, 160),
        "OpenFace": (96, 96),
        "DeepFace": (152, 152),
        "DeepID": (47, 55),
        "Dlib": (150, 150),
        "ArcFace": (112, 112),
        "SFace": (112, 112),
    }

    target_size = target_sizes.get(model_name)

    if target_size == None:
        raise ValueError(f"nome do modelo não implementado - {model_name}")

    return target_size


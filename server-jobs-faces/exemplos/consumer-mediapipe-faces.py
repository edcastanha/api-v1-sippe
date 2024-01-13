from deepface import DeepFace as Secedu
from datetime import datetime as dt
import os
import numpy as np
import cv2

# STEP 1: Import the necessary modules.
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


BACKEND_DETECTOR='retinaface'
#MODEL_BACKEND ='mtcnn'
MODEL_BACKEND ='Facenet'



LIMITE_DETECTOR = 0.995

#file = 'B:/SIPPE/FTP/sippe3/Sippe3/2023-09-04/001/jpg/13/28.47[M][0@0][0].jpg'
file = 'B:/SIPPE/FTP/img/people.jpg'

class ConsumerExtractor:
    def __init__(self):
        self.path_capture = 'capturas'

    def run(self):
        print(file)
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            now = dt.now()
            processamento = now.strftime("%Y-%m-%d %H:%M:%S")
            print(f'DIA: {processamento}')
   
            face_objs = Secedu.extract_faces(
                                        img_path=file,
                                        detector_backend=BACKEND_DETECTOR,
                                        enforce_detection=True,
                                        align=False
                                    )
            print(f'face_objs: {len(face_objs)}')

            for index, face_obj in enumerate(face_objs):
                print(f' <**_1_**>INDEX:: {index} {float(face_obj["confidence"])} >= {float(LIMITE_DETECTOR)} CONFIDENCE = {float(face_obj["confidence"]) >= float(LIMITE_DETECTOR)}')
                confidence = float(face_obj["confidence"])
                if confidence >= LIMITE_DETECTOR:
                    face = face_obj['face']
                    new_face = os.path.join(str(self.path_capture))
                    if not os.path.exists(new_face):
                        os.makedirs(new_face, exist_ok=True)

                    # Converta a imagem de float32 para uint8 (formato de imagem)
                    face_uint8 = (face * 255).astype('uint8')
                    
                    # Gere um nome de arquivo único para a face
                    save_path = os.path.join(new_face, f"face_{index}.jpg")
                    print(f' <**_5_**> SAVE NEW FACE Path:: {save_path}: ')
                
                    # Salve a face no diretório "captura/" usando OpenCV
                    cv2.imwrite(save_path, cv2.cvtColor(face_uint8, cv2.COLOR_RGB2BGR))
                    
                    
            # STEP 2: Criar um objeto FaceDetector.
            base_options = python.BaseOptions(model_asset_path='detector.tflite')
            options = vision.FaceDetectorOptions(base_options=base_options)
            detector = vision.FaceDetector.create_from_options(options)

            # STEP 3: Carregar a imagem de entrada.
            image = mp.Image.create_from_file(file)
            print(f'<**_6_**> IMAGE: {image}')
            # STEP 5: Process the detection result. In this case, visualize it.
            detection_result = detector.detect(image)
            print(f'<**_7_**>DETECTIONS: {detection_result}')

            # Itera sobre os resultados da detecção de rostos.
            for data in detection_result.detections:
                bounding_box = data.bounding_box
                categories = data.categories
                keypoints = data.keypoints

                # Imprime informações sobre cada detecção.
                print("Bounding Box:", bounding_box)
                
                for category in categories:
                    print("Category Index:", category.index)
                    print("Category Score:", category.score)
                
                for keypoint in keypoints:
                    print("Keypoint x:", keypoint.x)
                    print("Keypoint y:", keypoint.y)
                    print("Keypoint Label:", keypoint.label)
                    print("Keypoint Score:", keypoint.score)
                                    
            

    
if __name__ == "__main__":
    job = ConsumerExtractor()
    job.run()
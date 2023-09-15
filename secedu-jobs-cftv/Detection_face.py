import cv2
import os
import time
import datetime

#Class Local
import Publisher

#import tensorflow as tf
from retinaface import RetinaFace

# Configurando uso de GPU e limites de memória
# https://www.tensorflow.org/guide/gpu
# https://www.tensorflow.org/guide/gpu#limiting_gpu_memory_growth
publisher = Publisher()

#gpus = tf.config.list_physical_devices('GPU')

dir_img = "capturas/"
video = "B:/SIPPE/Videos/SimPlay20230829135807.dav"
rtsp = "rtsp://admin:ep4X1!br@192.168.15.200:554/user=admin_password=ep4X1!br_channel=0_stream=0.sdp?real_stream"


class CameraJob:
    def __init__(self, url = video, camera_id = 1):
        self.url = url
        self.camera_id = camera_id

    def run_task(self, intervalo = 5):
        try:
            cap = cv2.VideoCapture(self.url)

            while cap.isOpened():
                #print("Capturando frame...")
                ret, frame = cap.read()
                if not ret:
                    break
                pasta_criada = False
                
                #print("Faces detectadas:", detected_faces)
                detections = RetinaFace.detect_faces(frame,
                                                     threshold=0.98
                                                     )
                
                for face_key, face_data in detections.items():
                    score = face_data["score"]
                    facial_area = face_data["facial_area"]
                    right_eye = face_data["landmarks"]["right_eye"]
                    left_eye = face_data["landmarks"]["left_eye"]
                    nose = face_data["landmarks"]["nose"]
                    mouth_right = face_data["landmarks"]["mouth_right"]
                    mouth_left = face_data["landmarks"]["mouth_left"]
                # Imprimir ou fazer qualquer coisa com os valores
                    # print("Face key:", face_key)
                    # print("Score:", score)
                    # print("Facial area:", facial_area)
                    # print("Right eye:", right_eye)
                    # print("Left eye:", left_eye)
                    # print("Nose:", nose)
                    # print("Mouth right:", mouth_right)
                    # print("Mouth left:", mouth_left)
                    
                    # Realizar a rotina X apenas se houver dados nas variáveis
                    if score >=0.97 and right_eye and left_eye and nose and mouth_right and mouth_left:                    
                        #print(f"{face_key}: {facial_area}, confiança: {score}")
                        # Define as coordenadas da região de interesse
                        x1, y1, x2, y2 = facial_area[0], facial_area[1], facial_area[2], facial_area[3]

                        # Extrai a região de interesse
                        roi = frame[y1:y2, x1:x2]
                        #Definir nome da pasta
                        dia = datetime.datetime.now().strftime("%d-%m-%Y")
                        hora = datetime.datetime.now().strftime("%H")
                        minuto = datetime.datetime.now().strftime("%M")
                        if not pasta_criada:
                            os.makedirs(os.path.join(dir_img, dia, hora, minuto), exist_ok=True)
                            pasta_criada = True
                        data_path = os.path.join(dir_img, dia, hora, minuto)
                        # Verificar e criar o diretório
                        # Define o nome do arquivo de imagem
                        timestamp_str = datetime.datetime.now().strftime("%H-%M-%S")
                        snapshot_filename = f"{face_key}_{timestamp_str}.png"
                        
                        snapshot_path = os.path.join(dir_img, data_path, snapshot_filename)
                        #print(snapshot_path)
                        # Salva a imagem da região de interesse
                        cv2.imwrite(snapshot_path, roi)
                        
                        # Desenha um retângulo na imagem original
                        #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        #cv2.putText(frame, f"Face {i}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                        #cv2.putText(frame, f"Confiança: {confidence:.2f}", (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                        #cv2.imshow("Frame", frame)
                    
                        # Chama a classe RabbitMQPublisher para publicar na fila
                        #publisher.publish(snapshot_path, timestamp_str )
                            
                time.sleep(intervalo) # Intervalo entre as verificações de frame
            cap.release()
            cv2.destroyAllWindows()
        except Exception as e:
            print("Erro:", e)

if __name__ == '__main__':
    job = CameraJob()
    job.run_task(10)

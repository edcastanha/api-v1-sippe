import cv2
import os
import time
import datetime
from RabbitMQPublisher import RabbitMQPublisher
import tensorflow as tf
from deepface import DeepFace

# Configurando uso de GPU e limites de memória
# https://www.tensorflow.org/guide/gpu
# https://www.tensorflow.org/guide/gpu#limiting_gpu_memory_growth
publisher = RabbitMQPublisher()

gpus = tf.config.list_physical_devices('GPU')

dir_img = "B:\SIPPE\Capturas\Snapshot"
video = "B:/SIPPE/Videos/SimPlay20230829135807.dav"
rtsp = "rtsp://admin:ep4X1!br@192.168.15.200:554/user=admin_password=ep4X1!br_channel=0_stream=0.sdp?real_stream"


class ExtractFace:
    def __init__(self, intervalo, url , camera_id):
        self.intervalo = intervalo
        self.url = url
        self.camera_id = camera_id

    def run_task(self, ):
        try:
            print("Iniciando captura de frames...")
            cap = cv2.VideoCapture(self.url)

            while cap.isOpened():
                print("Read...")
                ret, frame = cap.read()
                if not ret:
                    break
                
                face_objs = DeepFace.extract_faces(frame,
                                                   enforce_detection=False,
                                                   )
                
                #print("Faces detectadas:", face_objs)
                #Percorre cada elemento da lista 'extracted_faces'
                for i, item in enumerate(face_objs):
                    face_key = f"face_{i + 1}"
                    face = item['face']
                    facial_area = item['facial_area']
                    confidence = item['confidence']
                    # Acessando os valores da chave 'facial_area'
                    x = item['facial_area']['x']
                    y = item['facial_area']['y']
                    w = item['facial_area']['w']
                    h = item['facial_area']['h']

                    # Realizar a rotina X apenas se houver dados nas variáveis
                    if confidence >= 9.5:
                        print(f"{face_key}: {facial_area}, confiança: {confidence}")
                        # Extrai a região de interesse
                        roi = frame[y:y+h, x:x+w]
                        #Definir nome da pasta
                
                        dia = datetime.datetime.now().strftime("%d-%m-%Y")
                        hora = datetime.datetime.now().strftime("%H")
                        minuto = datetime.datetime.now().strftime("%M")
                        os.makedirs(os.path.join(dir_img, self.camera_id, dia, hora, minuto), exist_ok=True)
                        data_path = os.path.join(dir_img, self.camera_id, dia, hora, minuto)
                        # Verificar e criar o diretório
                        # Define o nome do arquivo de imagem
                        timestamp_str = datetime.datetime.now().strftime("%H-%M-%S")
                        snapshot_filename = f"{face_key}_{timestamp_str}.png"
                        
                        snapshot_path = os.path.join(dir_img, data_path, snapshot_filename)
                        print(snapshot_path)
                        # Salva a imagem da região de interesse
                        cv2.imwrite(snapshot_path, roi)
                        
                        #
                    #cv2.imshow("Face", cv2.cvtColor(face, cv2.COLOR_BGR2RGB))
                    #cv2.waitKey(0)
                    #cv2.destroyAllWindows()
                    # Define as coordenadas da região de interesse
                    #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    #cv2.putText(frame, f"Face {i}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    #cv2.putText(frame, f"Confiança: {confidence:.2f}", (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    #cv2.imshow("Frame", frame)
                    
                        # Chama a classe RabbitMQPublisher para publicar na fila
                        #publisher.publish(snapshot_path, timestamp_str )
                            
                time.sleep(self.intervalo) # Intervalo entre as verificações de frame
            
            cap.release()
            cv2.destroyAllWindows()
        except Exception as e:
            print("Erro:", e)

if __name__ == '__main__':
    job = ExtractFace(intervalo=10, url="B:/SIPPE/Videos/SimPlay20230829135807.dav", camera_id="Sippe3")
    job.run_task()

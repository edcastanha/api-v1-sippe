import pika
import json
from retinaface import RetinaFace
import cv2
import os

dir_face = "B:\SIPPE\Capturas\Faces"

detectores = [
    "retinaface", 
    "mtcnn", 
    "dlib", 
    "opencv",
    ]
class RabbitMQConsumer:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=pika.PlainCredentials('sippe', 'ep4X1!br')))
        self.channel = self.connection.channel()
    
    def consume(self):
        def callback(ch, method, properties, body):
            # Deserializa a mensagem em um dicionário
            message_dict = json.loads(body)
            # Acessa os valores do dicionário
            snapshot_path = message_dict["snapshot_path"]
            timestamp = message_dict["timestamp"]   

            img = cv2.imread(snapshot_path)   

            faces = RetinaFace.detect_faces(snapshot_path, threshold=0.7)
            if faces is not None:
                # Pegar as coordenadas para criar novo retângulo e salvar a imagem da face
                print(faces)
                for i in range(len(faces)):
                    identity = faces[f"face_{i+1}"]
                    facial_area = identity["facial_area"]
                    landmarks = identity["landmarks"]
                    
                    #highlight facial area
                    cv2.rectangle(img, (facial_area[2], facial_area[3]), (facial_area[0], facial_area[1]), (255, 255, 255), 1)
                    
                    #extract facial area
                    #img = cv2.imread(img_path)
                    #facial_img = img[facial_area[1]: facial_area[3], facial_area[0]: facial_area[2]]
                    
                    #highlight the landmarks
                    cv2.circle(img, tuple(landmarks["left_eye"]), 1, (0, 0, 255), -1)
                    cv2.circle(img, tuple(landmarks["right_eye"]), 1, (0, 0, 255), -1)
                    cv2.circle(img, tuple(landmarks["nose"]), 1, (0, 0, 255), -1)
                    cv2.circle(img, tuple(landmarks["mouth_left"]), 1, (0, 0, 255), -1)
                    cv2.circle(img, tuple(landmarks["mouth_right"]), 1, (0, 0, 255), -1)

                    # Salva a imagem cortada no diretório "dir_face"
                    face_filename = f"Face_{i}_{timestamp}.png"
                    face_path = os.path.join(dir_face, face_filename)
                    cv2.imwrite(face_path, img)
            print("Mensagem recebida:")
            print(f"Snapshot path: {snapshot_path}")
            print(f"Timestamp: {timestamp}")
            print("##############################################")

            # Confirma o recebimento da mensagem
            #ch.basic_ack(delivery_tag=method.delivery_tag)


        self.channel.basic_consume(queue="detection_face", on_message_callback=callback, auto_ack=False)
        print("Aguardando mensagens...")
        self.channel.start_consuming()

    def close(self):
        self.connection.close()


if __name__ == '__main__':
    consumer = RabbitMQConsumer()
    consumer.consume()
    consumer.close()

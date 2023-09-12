import unittest
import os
import redis
from deepface import DeepFace
from face_rec_secedu.jobs.TrainningDbEmdding import DIR_DB_IMG, models

class TestTrainningRedis(unittest.TestCase):

    def setUp(self):
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

    def test_redis_connection(self):
        self.assertTrue(self.redis_client.ping())

    def test_embeddings(self):
        representations = []
        for dir_path, dir_name, file_names in os.walk(DIR_DB_IMG):
            for file_name in file_names:
                img_path = f"{dir_path}/{file_name}"
                if img_path.endswith((".png", ".jpg", ".jpeg")):  
                    embedding_obj = DeepFace.represent(
                        img_path=img_path, 
                        model_name = models[1], 
                        detector_backend='mtcnn',
                        enforce_detection=False
                        )
                    embedding = embedding_obj[0]["embedding"]
                    representations.append((img_path, embedding))
        for img_path, embedding in representations:
            self.assertTrue(self.redis_client.exists(f"embedding:{img_path}"))

if __name__ == '__main__':
    unittest.main()

import os
import redis
from redis.commands.search.field import VectorField, TagField
from redis.commands.search.query import Query
from deepface import DeepFace
import numpy as np
from tqdm import tqdm


import matplotlib.pyplot as plt

from publicar import Publisher
from loggingMe import logger

REDIS_SERVER = 'secedu-rds-tack'
RMQ_SERVER = 'secedu-rmq-task'
EXCHANGE='secedu'

QUEUE_PUBLISHIR='embedding'
ROUTE_KEY='verification'

QUEUE_CONSUMER='faces'
ASK_DEBUG = True

DIR_DATASET ='dataset'
BACKEND_DETECTOR='Facenet'
MODEL_BACKEND ='mtcnn'
LIMITE_DETECTOR =0.99

METRICS = ["cosine", "euclidean", "euclidean_l2"]

r = redis.StrictRedis(host=REDIS_SERVER, port=6379, db=0)

class ConsumerEmbbeding:
    
    logger.info(f' <**_ 1 _**> Server REDIS::{r.ping()}')
    embeddings = []
    for dirpath, dirnames, filenames in os.walk(DIR_DATASET):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            logger.info(f' <**_ 2 _**>  FOR PATH::{full_path}')

            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                embedding = DeepFace.represent(
                    img_path=full_path,
                    model_name="Facenet",
                    detector_backend="mtcnn",
                    enforce_detection=False,
                )[0]["embedding"]
                embeddings.append((full_path, embedding))
                logger.info(f' <**_ 3 _**> EMBEDDING FACE::{embedding}')

    if r.flushdb():
        pipeline = r.pipeline(transaction=False)
        for img_path, embedding in tqdm(embeddings):
            # Use os.path.basename para obter o último componente do caminho
            key = img_path
            value = np.array(embedding).astype(np.float32).tobytes()
            pipeline.hset(key, mapping = {"embedding": value})
            logger.info(f' <**_ 4 _**> KEY::{key}')

        # -------------------------------------
        pipeline_results = pipeline.execute()
        logger.info(f' <**_ REDIS _**> {pipeline_results}')

        r.ft().create_index(
            [
            VectorField(
                "embedding",
                "HNSW",
                {
                    "TYPE": "FLOAT32",
                    "DIM": 128,
                    "DISTANCE_METRIC": "L2",
                    },
                )
            ]
        )
        chaves = r.keys()
        logger.info(f' <**_ 5 _**> INDEX CREATE:: {chaves}')
        breakpoint
    else:
        logger.info(f' <**_ 5 _**> ERRO CREATE INDEX')

if __name__ == "__main__":
    ConsumerEmbbeding()

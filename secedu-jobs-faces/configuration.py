class Configuration:
    
    RMQ_SERVER = 'broker-server'
    RMQ_PORT = 5672
    RMQ_USER = 'secedu'
    RMQ_PASS = 'ep4X1!br'
    RMQ_EXCHANGE = 'secedu'
    
    REDIS_SERVER = 'redis-server'
    REDIS_PORT = 6379
    REDIS_DB = 0
    REDIS_SSL = False

    DIR_CAPS ='/app/media/capturas'
    DIR_DATASET ='/app/media/dataset'
    DIR_CAPTURE = '/app/media/capturas'

    BACKEND_DETECTOR = 'retinaface'
    MODEL_BACKEND = 'Facenet'
    DISTANCE_METRIC = 'euclidean_l2'
    ENFORCE_DETECTION = False

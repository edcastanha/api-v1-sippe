class Configuration:
    
    # ---------------------------------- RabbitMQ ----------------------------------
    RMQ_SERVER = 'broker-server'
    RMQ_PORT = 5672
    RMQ_USER = 'secedu'
    RMQ_PASS = 'ep4X1!br'
    RMQ_EXCHANGE = 'secedu'
    
    # ---------------------------------- REDIS ----------------------------------
    REDIS_SERVER = 'redis-server'
    REDIS_PORT = 6379
    REDIS_DB = 0
    REDIS_SSL = True
    # ---------------------------------- END REDIS ----------------------------------

    # ---------------------------------- PATH DIRS ----------------------------------
    DIR_CAPS ='/app/media/capturas'
    DIR_DATASET ='/app/media/dataset'
    DIR_CAPTURE = '/app/media/capturas'
    DIR_FACES_OVAL = '/app/media/faces-oval'
    # ---------------------------------- END PATH DIRS ----------------------------------


    # ---------------------------------- LIB FACE ----------------------------------
    BACKEND_DETECTOR = 'retinaface'
    MODEL_BACKEND = 'Facenet'
    DISTANCE_METRIC = 'euclidean'
    ENFORCE_DETECTION = False
    LIMITE_DETECTOR = 0.9
    LIMITE_AREA = 90
    # ---------------------------------- END LIB FACE ----------------------------------
import pika
from core.loggingMe import logger
from core.settings import RBMQ_HOST, RBMQ_PORT, RBMQ_USER, RBMQ_PASS

class Publisher:
    def __init__(self):
        logger.info('<**_ 1 _**> Inicializado: encaminha pastas de devices')
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RBMQ_HOST,
                port=RBMQ_PORT,
                credentials=pika.PlainCredentials(RBMQ_USER, RBMQ_PASS)
            )
        )
        self.channel = self.connection.channel()

    def start_publisher(self, exchange, routing_name, message):
        logger.info(f' <**_Publicando na Fila_ **> ROUTER_KEY:: {routing_name}')
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_name,
            body=message
        )

    # Queue Bind
    def bind_queue(self, queue_name, exchange, routing_key):
        logger.info(f' <**_Ligando na Fila_**> ROUTER_KEY:: {routing_key}')
        self.channel.queue_bind(
            queue=queue_name,
            exchange=exchange,
            routing_key=routing_key
        )

    def close(self):
        logger.info(f' <**_Fechando Comunicacao_**>')
        self.connection.close()

#if __name__ == '__main__':
#   
#    message = "/path/to/image.png"
#    timestamp = "2022-01-01 12:00:00"
#    queue_name = 'path_init'
#    capture_date = "2022-01-01"
#    device = "camera01"
#
#    # Configurações do Redis
#    redis_host = 'localhost'
#    redis_port = 6379
#
#    publisher = Publisher()
#    publisher.start_publisher(message, timestamp, queue_name)
#    publisher.close()

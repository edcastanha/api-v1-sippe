import pika
import json
from loggingMe import logger

class Publisher:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='localhost',
                port=5672,
                credentials=pika.PlainCredentials('secedu', 'ep4X1!br')
            )
        )
        self.channel = self.connection.channel()
        logger.info('<**_**> Inicializado Main: encaminha pastas de devices')

    def start_publisher(self, exchange, routing_name, message):
        self.channel.basic_publish(exchange=exchange, 
                                   routing_key=routing_name, 
                                   body=message)
        logger.info(f' <**_**> PUBLISHER : encaminha pastas de devices -ROUTER_KEY: {routing_name}')

    def close(self):
        logger.info(f' <**_**> CLOSE: Main')
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

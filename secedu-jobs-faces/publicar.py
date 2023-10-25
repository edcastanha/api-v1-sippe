import pika
import json
from loggingMe import logger

RMQ_SERVER = 'broker-server'

class Publisher:
    def __init__(self):
        self.routing = ''
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RMQ_SERVER,
                port=5672,
                credentials=pika.PlainCredentials('secedu', 'ep4X1!br')
            )
        )
        self.channel = self.connection.channel()

    def start_publisher(self, exchange, routing_name, message):
        try:
            self.channel.queue_declare(queue=routing_name, durable=True)
            self.routing = routing_name
            self.channel.basic_publish(exchange=exchange, 
                                    routing_key=routing_name, 
                                    body=message)
            logger.info(f' <**_PUBLISHER_ **> ROUTER_KEY:: {self.routing}')
            return True
        except Exception as e:
            logger.error(f' <**_PUBLISHER_ **> ROUTER_KEY:: {self.routing} - ERROR:: {e}')
            return False

    def close(self):
        logger.info(f' <**_CLOSE_**> ROUTER_KEY:: {self.routing}')
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

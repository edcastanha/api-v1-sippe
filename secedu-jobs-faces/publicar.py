import pika
import json
from loggingMe import logger
from configuration import Configuration


class Publisher:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=Configuration.RMQ_SERVER,
                port=Configuration.RMQ_PORT,
                credentials=pika.PlainCredentials(Configuration.RMQ_USER, Configuration.RMQ_PASS)
            )
        )
        self.channel = self.connection.channel()

    def start_publisher(self, exchange, queue_name, routing_name, message):
        try:
            self.channel.queue_declare(queue=queue_name, durable=True)
            self.channel.basic_publish(
                exchange=exchange, 
                routing_key=routing_name, 
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode = 2,
                )
            )
            logger.info(f' <**_PUBLISHER_ **> Mensagem enviada para fila: {queue_name} ')
        except Exception as e:
            logger.error(f' <**_PUBLISHER_ **> ERROR:: {e}')
    
    def close(self):
        if self.connection.is_open:
            self.connection.close()
            logger.info(f' <**_PUBLISHER_ **> Connection closed')
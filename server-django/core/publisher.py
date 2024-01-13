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
        self.properties = pika.BasicProperties(
            delivery_mode=2,  # 2 significa persistente
        )
        self.channel = self.connection.channel()

    def start_publisher(self, exchange, routing_name, message):
        logger.info(f' <**_Publicando na Fila_ **> ROUTER_KEY:: {routing_name}')
        try:
            self.channel.basic_publish(
                exchange=exchange,
                routing_key=routing_name,
                body=message,
                properties=self.properties
            )
        except Exception as e:
            logger.error(f' <**_Publisher_**> Erro ao Publicar::{str(e)}')
            self.close()

    # Queue Bind
    def bind_queue(self, queue_name, exchange, routing_key):
        logger.info(f' <**_Ligando na Fila_**> ROUTER_KEY:: {routing_key}')
        self.channel.queue_bind(
            queue=queue_name,
            exchange=exchange,
            routing_key=routing_key
        )

    def close(self):
        if self.channel.is_open:
            self.channel.close()
            logger.info(f' <**_Publisher_**> Fechando Canel Comunicacao')

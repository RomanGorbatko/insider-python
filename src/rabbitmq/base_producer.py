import pika

from config import rabbitmq


class BaseProducer:

    def __init__(self, consumer_name):
        self.consumer_name = consumer_name
        self.connection = None
        self.channel = None

        self.connect()

    def publish(self, body):
        consumer_config = rabbitmq.consumers[self.consumer_name]

        self.channel.basic_publish(
            exchange=consumer_config['exchange']['name'],
            routing_key=consumer_config['queue']['name'],
            body=body
        )

    def __del__(self):
        self.connection.close()

    def connect(self):
        credentials = pika.PlainCredentials(
            username=rabbitmq.credentials['user'],
            password=rabbitmq.credentials['pwd']
        )

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=rabbitmq.credentials['host'],
                credentials=credentials
            )
        )

        self.channel = self.connection.channel()

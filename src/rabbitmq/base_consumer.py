import abc
import pika
from config import rabbitmq


class BaseConsumer(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, consumer_name):
        self.consumer_name = consumer_name
        self.connection = None

    @abc.abstractmethod
    def callback(self, channel, method, properties, body):
        """Retrieve data from consumer"""

    def __del__(self):
        self.connection.close()

    def start(self):
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

        consumer_config = rabbitmq.consumers[self.consumer_name]

        channel = self.connection.channel()
        channel.exchange_declare(
            consumer_config['exchange']['name'],
            durable=consumer_config['exchange']['durable']
        )

        result = channel.queue_declare(
            consumer_config['queue']['name'],
            exclusive=consumer_config['queue']['exclusive'],
            durable=consumer_config['queue']['durable'],
        )

        channel.queue_bind(
            result.method.queue,
            exchange=consumer_config['exchange']['name']
        )

        channel.basic_consume(
            queue=result.method.queue,
            on_message_callback=self.callback,
            auto_ack=consumer_config['consumer']['autoAck']
        )

        channel.start_consuming()

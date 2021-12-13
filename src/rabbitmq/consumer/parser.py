import json
from abc import ABC
from src.rabbitmq.base_consumer import BaseConsumer


class ParserConsumer(BaseConsumer, ABC):
    def __init__(self):
        super().__init__('parser')

    @staticmethod
    def valid_worlds():
        return ['launch', 'inside']

    def callback(self, channel, method, properties, body):
        body = json.loads(body)
        text = body['text'].lower()

        valid_worlds_founded = []
        for valid_world in self.valid_worlds():
            if valid_world in text:
                valid_worlds_founded.append(valid_world)

        print(valid_worlds_founded)


if __name__ == "__main__":
    consumer = ParserConsumer()
    consumer.start()

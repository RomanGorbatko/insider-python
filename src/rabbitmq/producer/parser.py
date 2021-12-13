from src.rabbitmq.base_producer import BaseProducer


class ParserProducer(BaseProducer):
    def __init__(self):
        super().__init__('parser')

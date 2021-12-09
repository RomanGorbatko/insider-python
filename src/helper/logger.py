import logging


def logger():
    logging.basicConfig(
        format='%(threadName)s %(name)s %(levelname)s: %(message)s',
        level=logging.INFO)

    return logging

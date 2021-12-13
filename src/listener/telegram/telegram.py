import json
from pathlib import Path
from pyrogram import Client, filters
from config import telegram
from src.rabbitmq.producer.parser import ParserProducer


def get_text_from_message(original_message):
    if original_message.text:
        text = original_message.text
    else:
        text = original_message.caption

    return text


def run_listener():
    app = Client(
        'channel_listener_account',
        workdir=str(Path.cwd()) + '/../../../data/session',
        api_id=telegram.app['id'],
        api_hash=telegram.app['hash']
    )

    @app.on_message(filters.channel)
    def handler(client, message):
        try:
            if str(message.chat.id) in telegram.channels:
                # push to rabbit
                text = get_text_from_message(message)

                if text:
                    json_text = json.dumps({
                        'source': 'telegram',
                        'metaSource': message.chat.title,
                        'text': text
                    })

                    producer = ParserProducer()
                    producer.publish(body=json_text)
        except Exception as e:
            print(e)

    app.run()


if __name__ == "__main__":
    run_listener()

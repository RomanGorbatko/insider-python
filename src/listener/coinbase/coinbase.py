import feedparser
import threading
from datetime import datetime

from src.helper.logger import logger
from src.helper.lock import Lock

feed_url = "https://medium.com/feed/@coinbaseblog"
lock = Lock('coinbase', True)


def run_listener(interval=5.0):
    threading.Timer(interval, run_listener).start()

    feed = feedparser.parse(feed_url)

    last_feed = feed.entries[0]

    published_time = last_feed['published']
    published_title = last_feed['title']

    lock_name = published_time + published_title
    if not lock.exists():
        lock.create(lock_name)

    if not lock.exists(lock_name):
        # @todo raise processing event
        print('New item raised')
        print(lock.exists(lock_name))

        lock.clear()
        lock.create(lock_name)
        pass


run_listener()

import functools
import re
from bellchan.settings import Settings


def _is_match(message, pattern, flags):
    return bool(re.search(pattern, message.text, flags))


def _is_mentioned(message):
    is_mention = message.text.find(f'@{Settings.BOT_ID}') >= 0
    is_dm_channel = message.is_dm_channel()
    return is_mention or is_dm_channel


def listen_to(pattern, flags=0):
    def receive_func(func):
        @functools.wraps(func)
        def wrapper(bot, message):
            if not message.is_edited():
                if _is_match(message, pattern, flags):
                    func(bot, message)
        return wrapper
    return receive_func


def respond_to(pattern, flags=0):
    def receive_func(func):
        @functools.wraps(func)
        def wrapper(bot, message):
            if not message.is_edited():
                if _is_match(message, pattern, flags):
                    if _is_mentioned(message):
                        func(bot, message)
        return wrapper
    return receive_func

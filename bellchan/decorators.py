import functools
import re


def _is_match(message, pattern, flags):
    return bool(re.search(pattern, message.text, flags))


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
                    if message.is_mentioned():
                        func(bot, message)
        return wrapper
    return receive_func

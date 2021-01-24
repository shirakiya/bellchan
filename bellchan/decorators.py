import functools
import re


def _is_match(message, pattern: str, flags: int) -> bool:
    return bool(re.search(pattern, message.text, flags))


def respond_to(pattern: str, flags=0):
    def receive_func(func):
        @functools.wraps(func)
        def wrapper(send_func, web_client, message):
            if _is_match(message, pattern, flags):
                if message.is_mentioned():
                    func(send_func, web_client, message)
        return wrapper
    return receive_func

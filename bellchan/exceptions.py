class EventError(Exception):
    pass


class InvalidEventFormatError(EventError):
    pass


class HTMLTagNotFoundError(Exception):
    pass

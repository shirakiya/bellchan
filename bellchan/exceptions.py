class BellchanException(Exception):
    pass


class EventError(BellchanException):
    pass


class InvalidEventFormatError(EventError):
    pass


class HTMLTagNotFoundError(BellchanException):
    pass


class TokyoDomeTimeUnknownError(BellchanException):
    pass

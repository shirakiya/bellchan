from bellchan.exceptions import InvalidEventFormatError
from bellchan.settings import Settings


class Message(object):

    PROPS = (
        'type',
        'channel',
        'user',
        'text',
        'ts',
    )

    OPTIONAL_PROPS = (
        'edited',
    )

    @classmethod
    def is_valid(cls, event):
        if 'subtype' in event:
            return False
        if not all(prop in event for prop in cls.PROPS):
            return False
        return True

    def __init__(self, event):
        if not self.is_valid(event):
            raise InvalidEventFormatError('type==message')

        for k, v in event.items():
            if k in self.PROPS:
                setattr(self, k, v)

        self.edited = event['edited'] if 'edited' in event else None

    def __str__(self):
        return str(self.__dict__)

    def is_in_dm_channel(self):
        return self.channel.startswith('D')

    def is_asked(self):
        return f'@{Settings.BOT_ID}' in self.text

    def is_mentioned(self):
        return self.is_asked() or self.is_in_dm_channel()

    def is_edited(self):
        return bool(self.edited)

import re
from bellchan.utils.datetime_utils import get_now_day
from bellchan.utils.normalize_text import zen_to_han


class TokyoDomeSchedule(object):

    day_regexp = re.compile(r'\d+')

    def __init__(self, day, title, opening, start):
        self.day = self._extract_day_num(day)
        self.title = title if title else None
        self.opening = self._extract_time(opening) if opening else None
        self.start = self._extract_time(start) if start else None

    def __str__(self):
        return str(self.__dict__)

    def _extract_day_num(self, day):
        normalize_day = zen_to_han(str(day), kana=False, ascii=False)
        match = self.day_regexp.search(normalize_day)
        if not match:
            raise ValueError(f'Invalid day given. {day}')
        return int(match.group())

    def _extract_time(self, time):
        return zen_to_han(str(time), kana=False, digit=False)

    def has_program(self):
        return bool(self.title)

    def has_detail_time(self):
        return bool(self.opening) or bool(self.start)

    def has_start_time(self):
        return bool(self.start)

    def is_today(self):
        today = get_now_day()
        return self.day == today

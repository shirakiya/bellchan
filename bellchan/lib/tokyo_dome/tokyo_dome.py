import re

import requests
from bs4 import BeautifulSoup

from bellchan.exceptions import HTMLTagNotFoundError, TokyoDomeTimeUnknownError
from bellchan.utils.datetime_utils import get_now_day

from .schedule import TokyoDomeSchedule


class TokyoDome:

    URL = 'https://www.tokyo-dome.co.jp/dome/event/schedule.html'
    OPENTIME_REGEXP = re.compile(r'開催時間：(\d+:\d{2})[〜～](\d+:\d{2})')
    OPEN_REGEXP = re.compile(r'開場 (\d+:\d{2})')
    START_REGEXP = re.compile(r'開始 (\d+:\d{2})')

    def __init__(self):
        self._schedules = None

    @property
    def schedules(self):
        if self._schedules:
            return self._schedules

        self._schedules = self._get_schedules()

        return self._schedules

    def _get_page(self):
        res = requests.get(self.URL, timeout=10)
        res.encoding = 'UTF-8'
        return BeautifulSoup(res.text, 'lxml')

    def _get_schedules(self):
        page_bs = self._get_page()

        schedule_table_bs = page_bs.find('table', class_='c-mod-calender')
        if not schedule_table_bs:
            raise HTMLTagNotFoundError('Tokyo Dome schedule table is not found.')

        schedule_trs_bs = schedule_table_bs.find_all('tr', class_='c-mod-calender__item')
        if not schedule_trs_bs:
            raise HTMLTagNotFoundError('Tokyo Dome schedule tr is not found.')

        schedules = {}

        for schedule_tr_bs in schedule_trs_bs:
            schedule = self._build_schedule(schedule_tr_bs)
            if schedule:
                schedules[schedule.day] = schedule

        return schedules

    def _build_schedule(self, schedule_tr_bs):
        day_bs = schedule_tr_bs.find('th', class_='c-mod-calender__title')
        if not day_bs:
            return None
        day = day_bs.span.string.strip()  # "01"

        detail_cols_bs = schedule_tr_bs.find_all('div', class_='c-mod-calender__detail-col')
        if not detail_cols_bs:  # 予定なし
            return TokyoDomeSchedule(day=day, title=None, opening=None, start=None)

        title_bs = detail_cols_bs[1].find_all('p')[0]
        if title_bs.a:
            title = ' '.join(s.strip() for s in title_bs.a.strings)
        else:
            title = title_bs.string.strip()

        schedule_text = detail_cols_bs[1].find_all('p')[1].string
        if not schedule_text:  # スケジュールなし
            opening = None
            start = None
        else:
            schedule_text = schedule_text.strip()

            opentime_match = self.OPENTIME_REGEXP.search(schedule_text)
            open_match = self.OPEN_REGEXP.search(schedule_text)
            start_match = self.START_REGEXP.search(schedule_text)
            # pattern of '開始時間'
            if opentime_match:
                opening = '-'.join(opentime_match.groups())
                start = None
            # pattern of '開場 / 開始'
            elif open_match:
                opening = open_match.group(1)
                start = start_match.group(1) if start_match else None
            # pattern of '開始'
            elif start_match:
                opening = None
                start = start_match.group(1)
            else:
                raise TokyoDomeTimeUnknownError('Found unknown statement of schedule time.')

        return TokyoDomeSchedule(
            day=day,
            title=title,
            opening=opening,
            start=start,
        )

    def get_today_schedule(self):
        today = get_now_day()

        return self.schedules[today] if today in self.schedules else None

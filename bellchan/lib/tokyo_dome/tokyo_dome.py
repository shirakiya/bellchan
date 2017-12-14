import re
import requests
from bs4 import BeautifulSoup
from bellchan.exceptions import HTMLTagNotFoundError
from bellchan.lib.tokyo_dome.schedule import TokyoDomeSchedule


class TokyoDome(object):

    URL = 'https://www.tokyo-dome.co.jp/dome/schedule/'
    TITLE_REGEXP = re.compile(r'^title')

    def _get_page(self):
        res = requests.get(self.URL, timeout=10)
        res.encoding = 'UTF-8'
        return BeautifulSoup(res.text, 'lxml')

    def _build_schedule(self, schedule_tr_bs):
        day_bs = schedule_tr_bs.find('th')
        if not day_bs:
            # 1日に複数の予定がある場合はここに入る
            return None
        day = day_bs.string.strip()

        title_bs = schedule_tr_bs.find('div', class_=self.TITLE_REGEXP)
        if not title_bs:  # 予定無し
            return TokyoDomeSchedule(day=day, title=None, opening=None, start=None)

        title_p_bs = title_bs.find_all('p')[1]
        title = title_p_bs.a.string.strip() if title_p_bs.a else title_p_bs.string.strip()

        schedule_tds_bs = schedule_tr_bs.find_all('td')
        if not schedule_tds_bs:
            raise HTMLTagNotFoundError('Tokyo Dome schedule opening or start time cells are not found.')
        opening = schedule_tds_bs[0].string.strip() if schedule_tds_bs[0].string else None
        start = schedule_tds_bs[1].string.strip() if schedule_tds_bs[1].string else None

        return TokyoDomeSchedule(
            day=day,
            title=title,
            opening=opening,
            start=start,
        )

    def _get_table_records(self, page_bs):
        schedule_table_bs = page_bs.find('table', id='schedule_table')
        if not schedule_table_bs:
            raise HTMLTagNotFoundError('Tokyo Dome schedule table is not found.')

        schedule_trs_bs = schedule_table_bs.find_all('tr', class_='th_left')
        if not schedule_trs_bs:
            raise HTMLTagNotFoundError('Tokyo Dome schedule tr is not found.')

        return schedule_trs_bs

    def get_today_schedule(self):
        page_bs = self._get_page()
        for schedule_tr_bs in self._get_table_records(page_bs):
            schedule = self._build_schedule(schedule_tr_bs)
            if schedule and schedule.is_today():
                return schedule

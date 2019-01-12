from bellchan.lib.tokyo_dome import TokyoDome

from .base import BaseMessageBuilder


class TokyoDomeScheduleMessageBuilder(BaseMessageBuilder):

    def create(self):
        tokyo_dome = TokyoDome()
        tokyo_dome_schedule = tokyo_dome.get_today_schedule()

        if tokyo_dome_schedule:
            if tokyo_dome_schedule.has_program():
                message = '今日の東京ドームの予定は\n'
                message += f'- {tokyo_dome_schedule.title}'

                if tokyo_dome_schedule.has_detail_time():
                    if tokyo_dome_schedule.has_start_time():
                        message += f'（開始時刻: {tokyo_dome_schedule.start}）\n'
                    else:
                        message += f'（開催時間: {tokyo_dome_schedule.opening}）\n'
                else:
                    message += '（開催時間不明）\n'

                message += 'が開催されるみたいだよ！'
            else:
                message = '今日は東京ドームの予定はないみたい！'
        else:
            message = '今日の東京ドームの予定が見つからなかったよ。'

        return message

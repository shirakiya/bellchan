from bellchan.decorators import respond_to
from bellchan.lib.tokyo_dome import TokyoDome


@respond_to('今日の東京ドームの予定')
def tokyo_dome_schedule(bot, message):
    tokyo_dome = TokyoDome()
    tokyo_dome_schedule = tokyo_dome.get_today_schedule()

    if tokyo_dome_schedule:
        if tokyo_dome_schedule.has_program():
            text = '今日の東京ドームの予定は\n'
            text += f'- {tokyo_dome_schedule.title}'

            if tokyo_dome_schedule.is_known_time():
                text += '（開始時間： {}）\n'.format(', '.join([f'{s}〜' for s in tokyo_dome_schedule.starts]))
            else:
                text += '（開始時間不明）\n'

            text += 'が開催されるみたいだよ！'
        else:
            text = '今日は東京ドームの予定はないみたい！'
    # スケジュールが見つからなかった場合
    else:
        text = '今日の東京ドームの予定が見つからなかったよ。'

    bot.client.rtm_send_message(message.channel, text)

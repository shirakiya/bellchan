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

            if tokyo_dome_schedule.has_detail_time():
                if tokyo_dome_schedule.has_start_time():
                    text += f'（開始時刻: {tokyo_dome_schedule.start}）\n'
                else:
                    text += f'（開催時間: {tokyo_dome_schedule.opening}）\n'
            else:
                text += '（開催時間不明）\n'

            text += 'が開催されるみたいだよ！'
        else:
            text = '今日は東京ドームの予定はないみたい！'
    else:
        text = '今日の東京ドームの予定が見つからなかったよ。'

    bot.client.rtm_send_message(message.channel, text)

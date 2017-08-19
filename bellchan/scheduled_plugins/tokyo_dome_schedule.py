from bellchan.lib.tokyo_dome import TokyoDome


def notify_tokyo_dome_schedule(bot, schedule):

    def notify():
        tokyo_dome = TokyoDome()
        tokyo_dome_schedule = tokyo_dome.get_today_schedule()

        if tokyo_dome_schedule.has_program:
            text = '今日の東京ドームの予定は\n'
            text += f'{tokyo_dome_schedule.title}'
            text += '（開始時間： {}）\n'.format(' , '.join(tokyo_dome_schedule.starts))
            text += 'が開催されるみたいだよ！'
        else:
            text = '今日は東京ドームの予定はないみたい！'

        bot.push_message(text)

    for time in ('09:00', '19:00'):
        schedule.every().day.at(time).do(notify)

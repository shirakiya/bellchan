from bellchan.decorators import respond_to
from bellchan.message_builder import TokyoDomeScheduleMessageBuilder


@respond_to('今日の東京ドームの予定')
def tokyo_dome_schedule(bot, message):
    message_builder = TokyoDomeScheduleMessageBuilder()
    bot_message = message_builder.create()

    bot.send_message(message.channel, bot_message)

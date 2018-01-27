from bellchan.message_builder import MoneyForwardMessageBuilder


def notify_budget(bot, schedule, handle_schedule_error):

    @handle_schedule_error()
    def notify():
        message_builder = MoneyForwardMessageBuilder()
        bot_message = message_builder.create()

        bot.push_message(bot_message, with_channel=True)

    schedule.every().saturday.at('12:00').do(notify)

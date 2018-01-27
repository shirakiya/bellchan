from logging import getLogger
from bellchan.message_builder import MoneyForwardMessageBuilder

logger = getLogger(__name__)


def notify_budget(bot, schedule, handle_schedule_error):

    @handle_schedule_error()
    def notify():
        logger.info(f'Start scheduled function [notify_budget]')

        message_builder = MoneyForwardMessageBuilder()
        bot_message = message_builder.create()

        bot.push_message(bot_message, with_channel=True)

    schedule.every().saturday.at('12:00').do(notify)

from logging import getLogger

from bellchan.message_builder import TokyoDomeScheduleMessageBuilder
from bellchan.utils.work import parallel

logger = getLogger(__name__)


def notify_tokyo_dome_schedule(bot, schedule, handle_schedule_error):

    @handle_schedule_error()
    def notify():
        logger.info(f'Start scheduled function [notify_tokyo_dome_schedule]')

        message_builder = TokyoDomeScheduleMessageBuilder()
        bot_message = message_builder.create()

        bot.push_message(bot_message, with_channel=True)

    for time in ('09:00', '19:00'):
        schedule.every().day.at(time).do(parallel, notify)

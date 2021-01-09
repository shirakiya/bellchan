# This is an example of coding the schedule plugin.
'''
import time
from logging import getLogger

from bellchan.utils.work import parallel

logger = getLogger(__name__)


def example(bot, schedule, handle_schedule_error):

    @handle_schedule_error()
    def notify():
        logger.info('Start scheduled function [example]')

        for i in range(20):
            logger.info(f'sleep {i}')
            time.sleep(1)

        logger.info('This is an example for the scheduled plugin.')
        bot.push_message('This is an example for the scheduled plugin.')

    schedule.every().day.at('12:00').do(parallel, notify)
'''

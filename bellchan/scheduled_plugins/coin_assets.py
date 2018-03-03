from logging import getLogger
from bellchan.message_builder import CoinAssetsMessageBuilder

logger = getLogger(__name__)


def notify_coin_assets(bot, schedule, handle_schedule_error):

    @handle_schedule_error()
    def notify():
        logger.info(f'Start scheduled function [notify_coin_assets]')

        message_builder = CoinAssetsMessageBuilder()
        bot_message = message_builder.create()

        bot.push_message(bot_message, with_channel=True)

    schedule.every().day.at('09:05').do(notify)

import re
from bellchan.decorators import respond_to
from bellchan.message_builder import CoinAssetsMessageBuilder


@respond_to('coin_assets', re.IGNORECASE)
def coin_assets(bot, message):
    message_builder = CoinAssetsMessageBuilder()
    bot_message = message_builder.create()

    bot.send_message(message.channel, bot_message)

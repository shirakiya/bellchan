import re
from bellchan.decorators import respond_to


@respond_to('ping', re.IGNORECASE)
def ping(bot, message):
    bot.client.rtm_send_message(message.channel, 'PONGだよ！')

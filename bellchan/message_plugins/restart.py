import re

from bellchan.decorators import respond_to
from bellchan.lib.heroku import Heroku


@respond_to('restart', re.IGNORECASE)
def restart(bot, message):
    bot.send_message(message.channel, '再起動するよ！')

    Heroku.restart()

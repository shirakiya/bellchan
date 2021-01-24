import re

from slack_sdk.web.legacy_client import LegacyWebClient

from bellchan.decorators import respond_to
from bellchan.events import Message
from bellchan.lib.heroku import Heroku


@respond_to('restart', re.IGNORECASE)
def restart(send_func, web_client: LegacyWebClient, message: Message) -> None:
    send_func(web_client, message.channel, '再起動するよ！')

    Heroku.restart()

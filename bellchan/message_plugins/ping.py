import re

from slack_sdk.web.legacy_client import LegacyWebClient

from bellchan.decorators import respond_to
from bellchan.events import Message


@respond_to('ping', re.IGNORECASE)
def ping(send_func, web_client: LegacyWebClient, message: Message) -> None:
    send_func(web_client, message.channel, 'PONGだよ！')

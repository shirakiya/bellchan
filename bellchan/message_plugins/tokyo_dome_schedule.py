from slack_sdk.web.legacy_client import LegacyWebClient

from bellchan.decorators import respond_to
from bellchan.events import Message
from bellchan.message_builder import TokyoDomeScheduleMessageBuilder


@respond_to('今日の東京ドームの予定')
def tokyo_dome_schedule(send_func, web_client: LegacyWebClient, message: Message) -> None:
    message_builder = TokyoDomeScheduleMessageBuilder()
    bot_message = message_builder.create()

    send_func(web_client, message.channel, bot_message)

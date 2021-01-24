import functools
import traceback
from logging import getLogger

import schedule
from slack_sdk.rtm import RTMClient
from slack_sdk.web.legacy_client import LegacyWebClient

from bellchan import message_plugins, scheduled_plugins
from bellchan.events import Message
from bellchan.logger import setup_logger
from bellchan.settings import Settings

logger = getLogger(__name__)


class Bellchan:

    def __init__(self):
        setup_logger()

        self.settings = Settings
        self.rtm_client = RTMClient(token=self.settings.SLACK_API_TOKEN)
        self.web_client = LegacyWebClient(token=self.settings.SLACK_API_TOKEN)

        self.schedule = schedule
        for func in self.scheduled_plugins:
            func(self, self.schedule, self.handle_schedule_error)

            logger.info(f'Set schedule function [{func.__name__}]')

    @property
    def scheduled_plugins(self):
        return scheduled_plugins.__all__

    def push_message(self, text: str, with_channel: bool = False) -> None:
        if with_channel:
            text = f'<!channel> {text}'

        self.web_client.chat_postMessage(
            username=Settings.BOT_NAME,
            icon_url=Settings.BOT_ICON_URL,
            channel=Settings.DEFAULT_CHANNEL_ID,
            text=text,
        )

    def handle_schedule_error(self):
        def receive_func(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    handle_error(self.web_client, Settings.DEFAULT_CHANNEL_ID, e)
            return wrapper
        return receive_func

    def run(self):
        self.rtm_client.start()


@RTMClient.run_on(event="message")
def message(**payload) -> None:
    logger.info(f'receive message => {payload["data"]}')

    try:
        message = Message(Settings.BOT_ID, payload['data'])
    except Exception as e:
        logger.error(e)

    if not message.is_mentioned():
        return

    web_client = payload['web_client']

    for func in message_plugins.__all__:
        try:
            func(send_message, web_client, message)
        except Exception as e:
            handle_error(web_client, message.channel, e)


def send_message(web_client: LegacyWebClient, channel: str, text: str) -> None:
    web_client.chat_postMessage(
        username=Settings.BOT_NAME,
        icon_url=Settings.BOT_ICON_URL,
        channel=channel,
        text=text,
    )


def handle_error(web_client: LegacyWebClient, channel: str, e: Exception) -> None:
    text = 'エラーが起きちゃった...\n\n'
    text += '```\n{error}\n\n{trace_back}\n```'.format(**{
        'error': repr(e),
        'trace_back': traceback.format_exc().strip(),
    })

    send_message(web_client, channel, text)

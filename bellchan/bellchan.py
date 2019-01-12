import functools
import time
import traceback
from logging import getLogger

import schedule
from slackclient import SlackClient

from bellchan import message_plugins, scheduled_plugins
from bellchan.events import Message
from bellchan.logger import setup_logger
from bellchan.settings import Settings

logger = getLogger(__name__)


class Bellchan:

    def __init__(self):
        setup_logger()

        self.settings = Settings
        self.client = SlackClient(self.settings.SLACK_API_TOKEN)

        self.connection_success = False

        self.message_plugins = message_plugins.__all__
        self.scheduled_plugins = scheduled_plugins.__all__

        self.schedule = schedule
        for func in self.scheduled_plugins:
            func(self, self.schedule, self.handle_schedule_error)
            logger.info(f'Set schedule function [{func.__name__}]')

    def _connect(self):
        self.connection_success = self.client.rtm_connect(auto_reconnect=True)

        time.sleep(0.5)  # Wait for connecting to server with rtm_connect()

        if self.connection_success:
            logger.info('Connection success')
        else:
            logger.error('Connection failed.')

        return self.connection_success

    def is_connected(self):
        return self.connection_success

    def start_connection(self):
        self._connect()
        if self.is_connected():
            self.push_message('起動したよ！')

    def send_message(self, channel, text):
        if self.is_connected():
            self.client.rtm_send_message(channel, text)
            logger.info(f'send message => {text}')
        else:
            logger.error('Not connect Slack RTM.')

    def push_message(self, text, with_channel=False):
        if with_channel:
            text = f'<!channel> {text}'

        self.send_message(self.settings.DEFAULT_CHANNEL_ID, text)

    def handle_error(self, e):
        text = 'エラーが起きちゃった...\n\n'
        text += '```\n{error}\n\n{trace_back}\n```'.format(**{
            'error': repr(e),
            'trace_back': traceback.format_exc().strip(),
        })

        if self.is_connected():
            self.push_message(text)

        logger.error(text)

    def handle_schedule_error(self):
        def receive_func(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    self.handle_error(e)
            return wrapper
        return receive_func

    def run(self):
        self.start_connection()

        while True:
            self.schedule.run_pending()
            try:
                for event in self.client.rtm_read():
                    if not Message.is_valid(event):
                        continue
                    message = Message(event)
                    logger.info(f'receive message => {message}')
                    for func in self.message_plugins:
                        func(self, message)
            except Exception as e:
                self.handle_error(e)
            finally:
                time.sleep(1)

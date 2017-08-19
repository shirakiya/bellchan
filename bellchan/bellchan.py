import time
import traceback
from slackclient import SlackClient
import schedule

from bellchan.settings import Settings
from bellchan import message_plugins, scheduled_plugins
from bellchan.events.message import Message


class Bellchan(object):

    def __init__(self):
        self.settings = Settings
        self.client = SlackClient(self.settings.SLACK_API_TOKEN)
        self.connection_success = False

        self.message_plugins = message_plugins.__all__
        self.scheduled_plugins = scheduled_plugins.__all__

        self.schedule = schedule
        for func in self.scheduled_plugins:
            func(self, self.schedule)

    def connect(self):
        self.connection_success = self.client.rtm_connect()
        if self.connection_success:
            self.push_message('起動したよ！')
        else:
            print('Connection Failed.')

    def push_message(self, text):
        if self.connection_success:
            self.client.rtm_send_message(self.settings.DEFAULT_CHANNEL_ID, text)
        else:
            print('Not connect Slack RTM.')

    def handle_error(self, e):
        text = 'エラーが起きちゃった...\n\n'
        text += '```\n{error}\n\n{trace_back}\n```'.format(**{
            'error': repr(e),
            'trace_back': traceback.format_exc().strip(),
        })

        if self.connection_success:
            self.push_message(text)
        else:
            print(text)

    def run(self):
        self.connect()

        while True:
            try:
                self.schedule.run_pending()

                for event in self.client.rtm_read():
                    if not Message.is_valid(event):
                        continue
                    message = Message(event)
                    for func in self.message_plugins:
                        func(self, message)
            except Exception as e:
                self.handle_error(e)
            time.sleep(1)

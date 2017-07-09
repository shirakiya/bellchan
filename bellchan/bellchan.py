import time
import traceback
from slackclient import SlackClient
import schedule

from bellchan.settings import Settings
from bellchan import scheduled_plugins


class Bellchan(object):

    def __init__(self):
        self.settings = Settings
        self.client = SlackClient(self.settings.SLACK_API_TOKEN)
        self.connection_success = False

        self.schedule = schedule
        for func in scheduled_plugins.__all__:
            func(self.schedule, self)

    def connect(self):
        self.connection_success = self.client.rtm_connect()
        if self.connection_success:
            self.push_message('起動したよ！')
        else:
            print('Connection Failed.')

    def run(self):
        self.connect()

        while True:
            self.schedule.run_pending()
            try:
                for event in self.client.rtm_read():
                    if 'subtype' in event:
                        continue
                    if 'type' in event and event['type'] == 'message':
                        text = event['text']
                        is_mention = text.find(f'@{self.settings.BOT_ID}') >= 0
                        if not is_mention:
                            continue
                        user = event['user']
                        channel = event['channel']
                        reply_text = f'<@{user}> バファローベルだよ！'

                        self.client.rtm_send_message(channel, reply_text)
            except:
                print(traceback.format_exc())
            time.sleep(1)

    def push_message(self, text):
        if not self.connection_success:
            print('Not connect Slack RTM.')
            return
        self.client.rtm_send_message(self.settings.DEFAULT_CHANNEL_ID, text)

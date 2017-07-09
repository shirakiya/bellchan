import time
import traceback
from slackclient import SlackClient
from bellchan.settings import Settings


class Bellchan(object):

    def __init__(self):
        self.settings = Settings
        self.client = SlackClient(self.settings.SLACK_API_TOKEN)

    def connect(self):
        self.connection_success = self.client.rtm_connect()
        if self.connection_success:
            self.push_message('起動したよ！')
        else:
            print('Connection Failed.')

    def run(self):
        self.connect()

        while True:
            try:
                for event in self.client.rtm_read():
                    if 'subtype' in event:
                        continue
                    if 'type' in event and event['type'] == 'message':
                        channel = event['channel']
                        text = event['text']
                        is_mention = text.find(f'@{self.settings.BOT_ID}') >= 0
                        reply_text = 'バファローベルだよ！'
                        if is_mention:
                            user = event['user']
                            reply_text = f'<@{user}> {reply_text}'
                        self.client.rtm_send_message(channel, reply_text)
            except:
                print(traceback.format_exc())
            time.sleep(1)

    def push_message(self, text):
        self.client.rtm_send_message(self.settings.DEFAULT_CHANNEL_ID, text)

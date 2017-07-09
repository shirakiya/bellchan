import os


class Settings(object):

    SLACK_API_TOKEN = os.environ['SLACK_API_TOKEN']
    DEFAULT_CHANNEL_ID = os.environ['DEFAULT_CHANNEL_ID']
    BOT_ID = os.environ['BOT_ID']

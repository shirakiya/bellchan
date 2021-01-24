import os


class Settings:

    SLACK_API_TOKEN = os.environ['SLACK_API_TOKEN']
    DEFAULT_CHANNEL_ID = os.environ['DEFAULT_CHANNEL_ID']
    BOT_ID = os.environ['BOT_ID']
    BOT_NAME = os.environ['BOT_NAME']
    BOT_ICON_URL = os.environ['BOT_ICON_URL']

    REDIS_URL = os.environ['REDIS_URL']

    HEROKU_API_KEY = os.environ['HEROKU_API_KEY']

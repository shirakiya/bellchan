import os


class Settings(object):

    SLACK_API_TOKEN = os.environ['SLACK_API_TOKEN']
    DEFAULT_CHANNEL_ID = os.environ['DEFAULT_CHANNEL_ID']
    BOT_ID = os.environ['BOT_ID']

    REDIS_URL = os.environ['REDIS_URL']

    HEROKU_API_KEY = os.environ['HEROKU_API_KEY']

    ZAIF_API_KEY = os.environ['ZAIF_API_KEY']
    ZAIF_API_SECRET = os.environ['ZAIF_API_SECRET']

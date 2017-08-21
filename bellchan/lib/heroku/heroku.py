import requests
from bellchan.settings import Settings


class Heroku(object):

    URLS = {
        'restart': 'https://api.heroku.com/apps/bellchan/dynos/worker',
    }

    @classmethod
    def get_basic_headers(cls):
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/vnd.heroku+json; version=3',
            'Authorization': f'Bearer {Settings.HEROKU_API_KEY}',
        }

    @classmethod
    def restart(cls):
        requests.delete(cls.URLS['restart'], headers=cls.get_basic_headers())

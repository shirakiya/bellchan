from bellchan.lib.zaif.functions import get_assets
from .base import BaseMessageBuilder


class CoinAssetsMessageBuilder(BaseMessageBuilder):

    def create(self):
        assets = get_assets()
        message = f'今の仮想通貨建て保有資産は{assets}円だよ！'

        return message

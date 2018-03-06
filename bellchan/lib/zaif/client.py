import copy
import hashlib
import hmac
from logging import getLogger
from urllib.parse import urlencode
import requests
from bellchan.exceptions import (
    ZaifCredentialsError,
    ZaifResponseError,
)
from bellchan.settings import Settings
from .nonce import ZaifNonce

logger = getLogger(__name__)


class ZaifClient:

    CURRENCY_PAIRS_URL = 'https://api.zaif.jp/api/1/currency_pairs/'
    LAST_PRICE_URL = 'https://api.zaif.jp/api/1/last_price/'
    TRADE_URL = 'https://api.zaif.jp/tapi'

    TIMEOUT = 30

    def __init__(self):
        self._call_trade_api_count = 0

        self._key = Settings.ZAIF_API_KEY
        self._secret = Settings.ZAIF_API_SECRET

        if not self._key or not self._secret:
            raise ZaifCredentialsError('Credentials of Zaif is not set.')

        self._base_signature = self._get_signature(self._secret)
        self._nonce = ZaifNonce()

    def _get_signature(self, string):
        return hmac.new(bytearray(string, encoding='utf-8'), digestmod=hashlib.sha512)

    def _call_public_api(self, url):
        logger.info(f'GET request to {url}')

        res = requests.get(url, timeout=self.TIMEOUT)

        if res.status_code != requests.codes.ok:
            res.raise_for_status()

        return res.json()

    def _build_params(self, method):
        nonce = self._nonce.get()
        logger.info(f'Use nonce {nonce}')

        return {
            'nonce': nonce,
            'method': method,
        }

    def _build_encoded_params(self, method):
        return urlencode(self._build_params(method))

    def _build_headers(self, encoded_params):
        signature = copy.copy(self._base_signature)
        signature.update(encoded_params.encode('utf-8'))

        return {
            'key': self._key,
            'sign': signature.hexdigest(),
        }

    def _call_trade_api(self, url, method):
        logger.info(f'POST request to {url} with {method}')

        encoded_params = self._build_encoded_params(method)
        headers = self._build_headers(encoded_params)

        try:
            self._call_trade_api_count += 1
            res = requests.post(url, data=encoded_params, headers=headers, timeout=self.TIMEOUT)
        except requests.Timeout as e:
            if self._call_trade_api_count < 5:
                return self._call_trade_api(url, method)
            else:
                raise

        if res.status_code != requests.codes.ok:
            logger.error(f'Something error occured when call to Trade API. Response body => {res.text}')
            res.raise_for_status()

        return res.json()

    def _post_trade(self, url, method):
        res_data = self._call_trade_api(url, method)

        if res_data.get('success'):
            return res_data['return']
        else:
            error_message = res_data['error']
            raise ZaifResponseError(error_message)

    def get_all_currency_pairs(self):
        url = self.CURRENCY_PAIRS_URL + 'all'
        return self._call_public_api(url)

    def get_last_price(self, currency_pairs):
        url = self.LAST_PRICE_URL + currency_pairs
        return self._call_public_api(url)

    def get_info2(self):
        url = self.TRADE_URL
        return self._post_trade(url, 'get_info2')

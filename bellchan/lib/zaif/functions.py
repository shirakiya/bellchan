from bellchan.lib.zaif.client import ZaifClient

CURRENCY_PAIRS_MAPPING = {
    'btc': 'btc_jpy',
    'ETH': 'eth_jpy',
    'mona': 'mona_jpy',
    'xem': 'xem_jpy',
}


def get_assets():
    assets = 0
    zaif_client = ZaifClient()

    user_info = zaif_client.get_info2()
    funds = user_info['funds']

    assets += funds['jpy']

    for currency, currency_pair in CURRENCY_PAIRS_MAPPING.items():
        quantity = funds[currency]
        if quantity <= 0:
            continue

        last_price = zaif_client.get_last_price(currency_pair)['last_price']
        assets += quantity * last_price

    return assets

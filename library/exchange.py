import logging
import re
from decimal import Decimal
from enum import Enum

import requests

logger = logging.getLogger(__name__)


# TODO: Add blockchain.info
#  * https://www.blockchain.com/api/exchange_rates_api
#  * https://blockchain.info/ticker

class ExchangeEnum(Enum):
    # Enum name = Exchange name(Fiat name)
    GDAX_USD = 'GDAX(USD)'
    BITFLYER_JPY = 'bitFlyer(JPY)'

    @staticmethod
    def get_value_list():
        return list(map(lambda x: x.value, ExchangeEnum))

    def get_fiat_name(self):
        fiat_name = re.search(
            r'\((\w+)\)',  # Searches `(word)` and sets `word` in group 1
            self.value  # e.g. 'GDAX(USD)'
        ).group(1)
        return fiat_name


class Exchange:
    """
    Fetch btc price from exchanges.
    """

    NETWORK_TIMEOUT = 10

    def __init__(self, exchange_enum: ExchangeEnum = ExchangeEnum.GDAX_USD):
        self._exchange_enum = exchange_enum

    def get_exchange_enum(self):
        return self._exchange_enum

    def fetch_btc_price(self) -> int:
        if self._exchange_enum == ExchangeEnum.GDAX_USD:
            return self._fetch_from_gdax()
        if self._exchange_enum == ExchangeEnum.BITFLYER_JPY:
            return self._fetch_from_bitflyer()

    def _fetch_from_gdax(self) -> int:
        url = 'https://api.pro.coinbase.com/products/BTC-USD/ticker'
        response = requests.get(url, timeout=self.NETWORK_TIMEOUT)
        if not response:
            raise ExchangeException('No response received from {}'.format(self._exchange_enum.value))
        json_data = response.json()
        price = int(Decimal(json_data['price']) * 100)
        return price

    def _fetch_from_bitflyer(self) -> int:
        url = 'https://api.bitflyer.com/v1/executions'
        params = {
            'product_code': 'BTC_JPY',
            'count': 1,
        }
        response = requests.get(url, params, timeout=self.NETWORK_TIMEOUT)
        if not response:
            raise ExchangeException('No response received from {}'.format(self._exchange_enum.value))
        json_data = response.json()
        price = int(json_data[0]['price'])
        return price


class ExchangeException(Exception):
    pass

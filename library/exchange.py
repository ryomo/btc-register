import logging
from decimal import Decimal
from typing import List

import requests

logger = logging.getLogger(__name__)


class Exchange:
    """
    Fetch btc price from exchanges.
    """

    NETWORK_TIMEOUT = 10

    exchanges = {
        'Blockchain': ['USD', 'AUD', 'BRL', 'CAD', 'CHF', 'CLP', 'CNY', 'DKK', 'EUR', 'GBP', 'HKD', 'INR', 'ISK', 'JPY',
                       'KRW', 'NZD', 'PLN', 'RUB', 'SEK', 'SGD', 'THB', 'TWD'],
        'GDAX': ['USD'],
        'bitFlyer': ['JPY'],
    }

    def __init__(self, name: str = 'Blockchain', fiat_name: str = 'USD', fiat_fractional_digits: int = 2):

        # If specified `name` is not valid, one exchange in `self.exchanges` will be set.
        if name not in self.exchanges.keys():
            name = list(self.exchanges.keys())[0]

        # If specified `fiat_name` is not valid, the first fiat in `self.exchanges[name]` will be set.
        if fiat_name not in self.exchanges[name]:
            fiat_name = self.exchanges[name][0]

        self.name = name
        self.fiat_name = fiat_name
        self.fiat_fractional_digits = fiat_fractional_digits

    @staticmethod
    def get_exchange_list(fiat_name=None) -> List[str]:
        """
        Get exchange name's list.
        If fiat_name is specified, exchanges corresponding to it are returned.
        :param fiat_name: e.g.) 'USD'
        :return: e.g.) ['Blockchain', 'GDAX']
        """
        if fiat_name:
            exchange_list = list(key for key, value in Exchange.exchanges.items() if fiat_name in value)
        else:
            exchange_list = list(Exchange.exchanges.keys())

        return sorted(exchange_list)

    def fetch_btc_price(self) -> int:
        """
        Fetch btc price from the exchange.
        :return: In cents, not in dollars.
        """
        if self.name == 'Blockchain':
            return self._fetch_from_blockchain(self.fiat_name)
        if self.name == 'GDAX':
            return self._fetch_from_gdax()
        if self.name == 'bitFlyer':
            return self._fetch_from_bitflyer()

    def _fetch_from_blockchain(self, fiat_name: str) -> int:
        url = 'https://blockchain.info/ticker'
        response = requests.get(url, timeout=self.NETWORK_TIMEOUT)
        if not response:
            raise ExchangeException('No response received from {}'.format(self.name))
        json_data = response.json()
        price = Decimal(json_data[fiat_name]['last']) * 10 ** self.fiat_fractional_digits
        return int(price)

    def _fetch_from_gdax(self) -> int:
        url = 'https://api.pro.coinbase.com/products/BTC-USD/ticker'
        response = requests.get(url, timeout=self.NETWORK_TIMEOUT)
        if not response:
            raise ExchangeException('No response received from {}'.format(self.name))
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
            raise ExchangeException('No response received from {}'.format(self.name))
        json_data = response.json()
        price = int(json_data[0]['price'])
        return price


class ExchangeException(Exception):
    pass

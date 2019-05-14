import logging
from decimal import Decimal
from typing import List

logger = logging.getLogger(__name__)


class Fiat:
    fiats = {
        'AUD': {'symbol': '$', 'fractional_digits': 2},    # Australian dollar
        'BRL': {'symbol': 'R$', 'fractional_digits': 2},   # Brazilian real
        'CAD': {'symbol': '$', 'fractional_digits': 2},    # Canadian dollar
        'CHF': {'symbol': 'CHF', 'fractional_digits': 2},  # Swiss franc
        'CLP': {'symbol': '$', 'fractional_digits': 0},    # Chilean peso
        'CNY': {'symbol': '¥', 'fractional_digits': 2},    # Chinese yuan
        'DKK': {'symbol': 'kr', 'fractional_digits': 2},   # Danish krone
        'EUR': {'symbol': '€', 'fractional_digits': 2},    # Euro
        'GBP': {'symbol': '£', 'fractional_digits': 2},    # Pound sterling
        'HKD': {'symbol': '$', 'fractional_digits': 2},    # Hong Kong dollar
        'INR': {'symbol': '₹', 'fractional_digits': 2},    # Indian rupee
        'ISK': {'symbol': 'kr', 'fractional_digits': 0},   # Icelandic króna
        'JPY': {'symbol': '¥', 'fractional_digits': 0},    # Japanese yen
        'KRW': {'symbol': '₩', 'fractional_digits': 0},    # South Korean won
        'NZD': {'symbol': '$', 'fractional_digits': 2},    # New Zealand dollar
        'PLN': {'symbol': 'zł', 'fractional_digits': 2},   # Polish złoty
        'RUB': {'symbol': 'RUB', 'fractional_digits': 2},  # Russian rouble
        'SEK': {'symbol': 'kr', 'fractional_digits': 2},   # Swedish krona
        'SGD': {'symbol': '$', 'fractional_digits': 2},    # Singapore dollar
        'THB': {'symbol': '฿', 'fractional_digits': 2},    # Thai baht
        'TWD': {'symbol': 'NT', 'fractional_digits': 2},   # New Taiwan dollar
        'USD': {'symbol': '$', 'fractional_digits': 2},    # United States dollar
    }

    def __init__(self, fiat_name: str):

        # 'USD', 'JPY', ...
        self.name = fiat_name  # type: str

        # '$', '¥', ...
        self.symbol = self.fiats[self.name]['symbol']  # type: str

        #  the number of fractional digits after a decimal point
        self.frac_digits = self.fiats[self.name]['fractional_digits']  # type: int

    @staticmethod
    def get_fiat_list() -> List[str]:
        return sorted(list(Fiat.fiats.keys()))

    def cent_to_dollar(self, cent: int) -> Decimal:
        if cent == 0:
            return Decimal(0)

        return (Decimal(cent) / 10 ** self.frac_digits).quantize(Decimal('0.1') ** self.frac_digits)

    def dollar_to_cent(self, dollar: Decimal) -> int:
        return int(dollar * 10 ** self.frac_digits)

    def has_dot(self) -> bool:
        if self.frac_digits > 0:
            return True
        else:
            return False

from decimal import Decimal


class Fiat:

    def __init__(self, fiat_name: str):
        fiats = {
            'EUR': {'symbol': '€', 'fractional_digits': 2},
            'JPY': {'symbol': '¥', 'fractional_digits': 0},
            'USD': {'symbol': '$', 'fractional_digits': 2},
        }

        # 'USD', 'JPY', ...
        self.name = fiat_name  # type: str

        # '$', '¥', ...
        self.symbol = fiats[self.name]['symbol']  # type: str

        #  the number of fractional digits after a decimal point
        self.frac_digits = fiats[self.name]['fractional_digits']  # type: int

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

from decimal import Decimal


class Fiat:

    def __init__(self, fiat_name: str):
        self.name = fiat_name  # type: str  # 'USD', 'JPY', ...
        self.mark = ...  # type: str  # '$', '¥', ...

        if self.name == 'USD':
            self.mark = '$'

        elif self.name == 'JPY':
            self.mark = '¥'

        else:
            raise ValueError('Invalid fiat name')

    def cent_to_dollar(self, cent: int) -> Decimal:
        if self.name == 'USD':
            if cent == 0:
                return Decimal(0)
            return (Decimal(cent) / 100).quantize(Decimal('0.01'))

        elif self.name == 'JPY':
            return Decimal(cent)

        else:
            raise ValueError

    def dollar_str_to_cent(self, dollar: str) -> int:
        if self.name == 'USD':
            return int(Decimal(dollar) * 100)

        elif self.name == 'JPY':
            return int(dollar)

        else:
            raise ValueError

    def has_dot(self) -> bool:
        if self.name == 'USD':
            return True

        elif self.name == 'JPY':
            return False

        else:
            raise ValueError

    def max_digits_after_point(self) -> int:
        if self.name == 'USD':
            return 2

        elif self.name == 'JPY':
            return 0

        else:
            raise ValueError

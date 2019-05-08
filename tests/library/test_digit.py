import locale
from decimal import Decimal
from unittest import TestCase

from library.digit import Digit


class TestDigit(TestCase):

    def test_format(self):
        from library.fiat import Fiat

        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        digit = Digit()
        fiat = Fiat('USD')
        self.assertEqual(digit.format(Decimal('1234.56'), fiat.frac_digits), '1,234.56')

        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
        digit = Digit()
        fiat = Fiat('EUR')
        self.assertEqual(digit.format(Decimal('1234.56'), fiat.frac_digits), '1 234,56')

        locale.setlocale(locale.LC_ALL, 'ja_JP.UTF-8')
        digit = Digit()
        fiat = Fiat('JPY')
        self.assertEqual(digit.format(Decimal('123456'), fiat.frac_digits), '123,456')

    def test_get_decimal_point(self):
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        digit = Digit()
        self.assertEqual(digit.get_decimal_point(), '.')

        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
        digit = Digit()
        self.assertEqual(digit.get_decimal_point(), ',')

        locale.setlocale(locale.LC_ALL, 'ja_JP.UTF-8')
        digit = Digit()
        self.assertEqual(digit.get_decimal_point(), '.')

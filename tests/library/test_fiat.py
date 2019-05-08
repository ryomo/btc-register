from decimal import Decimal
from unittest import TestCase

from localize.fiat import Fiat


class TestFiat(TestCase):

    def test_name(self):
        fiat = Fiat('EUR')
        self.assertEqual(fiat.name, 'EUR')

        fiat = Fiat('JPY')
        self.assertEqual(fiat.name, 'JPY')

        fiat = Fiat('USD')
        self.assertEqual(fiat.name, 'USD')

    def test_symbol(self):
        fiat = Fiat('EUR')
        self.assertEqual(fiat.symbol, '€')

        fiat = Fiat('JPY')
        self.assertEqual(fiat.symbol, '¥')

        fiat = Fiat('USD')
        self.assertEqual(fiat.symbol, '$')

    def test_frac_digits(self):
        fiat = Fiat('EUR')
        self.assertEqual(fiat.frac_digits, 2)

        fiat = Fiat('JPY')
        self.assertEqual(fiat.frac_digits, 0)

        fiat = Fiat('USD')
        self.assertEqual(fiat.frac_digits, 2)

    def test_cent_to_dollar(self):
        fiat = Fiat('EUR')
        self.assertEqual(fiat.cent_to_dollar(100), Decimal('1'))
        self.assertEqual(fiat.cent_to_dollar(123), Decimal('1.23'))

        fiat = Fiat('JPY')
        self.assertEqual(fiat.cent_to_dollar(100), Decimal('100'))
        self.assertEqual(fiat.cent_to_dollar(123), Decimal('123'))

        fiat = Fiat('USD')
        self.assertEqual(fiat.cent_to_dollar(100), Decimal('1'))
        self.assertEqual(fiat.cent_to_dollar(123), Decimal('1.23'))

    def test_dollar_to_cent(self):
        fiat = Fiat('EUR')
        self.assertEqual(fiat.dollar_to_cent(Decimal('1.23')), 123)
        self.assertEqual(fiat.dollar_to_cent(Decimal('1.234')), 123)

        fiat = Fiat('JPY')
        self.assertEqual(fiat.dollar_to_cent(Decimal('123')), 123)

        fiat = Fiat('USD')
        self.assertEqual(fiat.dollar_to_cent(Decimal('1.23')), 123)
        self.assertEqual(fiat.dollar_to_cent(Decimal('1.234')), 123)

    def test_has_dot(self):
        fiat = Fiat('EUR')
        self.assertTrue(fiat.has_dot())

        fiat = Fiat('JPY')
        self.assertFalse(fiat.has_dot())

        fiat = Fiat('USD')
        self.assertTrue(fiat.has_dot())

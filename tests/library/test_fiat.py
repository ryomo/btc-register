from decimal import Decimal
from unittest import TestCase

from library.fiat import Fiat


class TestFiat(TestCase):

    def test_name(self):
        fiat = Fiat('USD')
        self.assertEqual(fiat.name, 'USD')

        fiat = Fiat('JPY')
        self.assertEqual(fiat.name, 'JPY')

    def test_mark(self):
        fiat = Fiat('USD')
        self.assertEqual(fiat.mark, '$')

        fiat = Fiat('JPY')
        self.assertEqual(fiat.mark, '¥')

    def test_cent_to_dollar(self):
        fiat = Fiat('USD')
        self.assertEqual(fiat.cent_to_dollar(100), Decimal('1'))
        self.assertEqual(fiat.cent_to_dollar(123), Decimal('1.23'))

        fiat = Fiat('JPY')
        self.assertEqual(fiat.cent_to_dollar(100), Decimal('100'))
        self.assertEqual(fiat.cent_to_dollar(123), Decimal('123'))

    def test_dollar_str_to_cent(self):
        fiat = Fiat('USD')
        self.assertEqual(fiat.dollar_str_to_cent('1.23'), 123)
        self.assertEqual(fiat.dollar_str_to_cent('1.234'), 123)

        fiat = Fiat('JPY')
        self.assertEqual(fiat.dollar_str_to_cent('123'), 123)

    def test_has_dot(self):
        fiat = Fiat('USD')
        self.assertTrue(fiat.has_dot())

        fiat = Fiat('JPY')
        self.assertFalse(fiat.has_dot())

    def test_max_digits_after_point(self):
        fiat = Fiat('USD')
        self.assertEqual(fiat.max_digits_after_point(), 2)

        fiat = Fiat('JPY')
        self.assertEqual(fiat.max_digits_after_point(), 0)

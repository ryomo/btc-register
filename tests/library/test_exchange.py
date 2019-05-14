from unittest import TestCase

from library.exchange import Exchange


class TestExchange(TestCase):

    def test_get_exchange_list(self):
        self.assertEqual(Exchange.get_exchange_list(), ['GDAX', 'bitFlyer'])

        self.assertEqual(Exchange.get_exchange_list('USD'), ['GDAX'])
        self.assertEqual(Exchange.get_exchange_list('JPY'), ['bitFlyer'])
        self.assertEqual(Exchange.get_exchange_list('AUD'), [])
        self.assertEqual(Exchange.get_exchange_list('NOTHING'), [])

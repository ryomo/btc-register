from unittest import TestCase

from library.exchange import Exchange


class TestExchange(TestCase):

    def test_get_exchange_list(self):
        self.assertEqual(Exchange.get_exchange_list(), ['Blockchain', 'GDAX', 'bitFlyer'])

        self.assertEqual(Exchange.get_exchange_list('USD'), ['Blockchain', 'GDAX'])
        self.assertEqual(Exchange.get_exchange_list('JPY'), ['Blockchain', 'bitFlyer'])
        self.assertEqual(Exchange.get_exchange_list('AUD'), ['Blockchain'])
        self.assertEqual(Exchange.get_exchange_list('NOTHING'), [])

import datetime
import json
import os
import pathlib
from unittest import TestCase

from requests import Response

from api.lnd import Lnd


class TestLnd(TestCase):

    def setUp(self):
        self.lnd = Lnd(
            'https://localhost:8080',
            '~/.lnd/tls.cert',
            '~/.lnd/data/chain/bitcoin/testnet/admin.macaroon'
        )

        # Reads password
        tests_dir = os.path.dirname(os.path.abspath(__file__)) + '/../'
        try:
            wallet_password = pathlib.Path(tests_dir + '.secret').read_text()
        except FileNotFoundError:
            self.fail('Write your wallet password at `tests/.secret`')
        self.lnd.unlock_wallet(wallet_password)

    def test_getinfo(self):
        self.assertIsNotNone(self.lnd.getinfo())

    def test_add_invoice_and_subscribe_invoices(self):
        invoice_memo = '[{}] test'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        json_data = None

        def callback(stream_response: Response):
            nonlocal json_data
            for raw_data in stream_response.iter_lines():
                json_data = json.loads(raw_data.decode())
                # print(json_data)
                """
                (json_data before payment e.g.)
                {
                    'result': {
                        'payment_request': 'lntb249790n1pwztadvpp5cefc0cac0fnc3n39p7n9rmh9msgqd854ln879e6wvp54f6jzc...',
                        'add_index': '103',
                        'expiry': '180',
                        'creation_date': '1545991596',
                        'memo': 'description test',
                        'r_preimage': '01SXFpPfsOuPJqtBLEXwOLnPu6SroZwCyqVcCbbD2UE=',
                        'value': '24979',
                        'cltv_expiry': '144',
                        'r_hash': 'xlOH47h6Z4jOJQ+mUe7l3BAGnpX8z+LnTmBpVOpCxjA='
                    }
                }
                
                (json_data after payment e.g.)
                {
                    'result': {
                        'amt_paid_sat': '24979',
                        'payment_request': 'lntb249790n1pwztadvpp5cefc0cac0fnc3n39p7n9rmh9msgqd854ln879e6wvp54f6jzc...',
                        'amt_paid_msat': '24979000',
                        'memo': 'description test',
                        'r_preimage': '01SXFpPfsOuPJqtBLEXwOLnPu6SroZwCyqVcCbbD2UE=',
                        'value': '24979',
                        'cltv_expiry': '144',
                        'expiry': '180',
                        'settle_index': '12',
                        'amt_paid': '24979000',
                        'creation_date': '1545991596',
                        'add_index': '103',
                        'settled': True,
                        'r_hash': 'xlOH47h6Z4jOJQ+mUe7l3BAGnpX8z+LnTmBpVOpCxjA=',
                        'settle_date': '1545991627'
                    }
                }
                """
                if json_data['result']['memo'] == invoice_memo:
                    return

        r_hash, add_index, payment_request = self.lnd.add_invoice(100, invoice_memo)

        subscribe_invoices_thread = self.lnd.create_subscribe_invoices_thread(callback, add_index - 1)
        subscribe_invoices_thread.start()

        subscribe_invoices_thread.join()

        self.assertEqual(json_data['result']['memo'], invoice_memo)
        self.assertEqual(json_data['result']['r_hash'], r_hash)
        self.assertEqual(int(json_data['result']['add_index']), add_index)
        self.assertEqual(json_data['result']['payment_request'], payment_request)

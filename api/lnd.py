import base64
import codecs
import json
import logging
import os
from typing import Callable, List

import requests
from requests import Response

from api.lnd_stream_thread import LndStreamThread

logger = logging.getLogger(__name__)


class Lnd:
    """
    https://api.lightning.community/rest/index.html?python
    """
    TIMEOUT = 10  # Note: 3 is not enough to unlock the wallet.
    URL_SUFFIX = '/v1/'

    def __init__(self, url, cert_path, macaroon_path):
        """
        :param url: e.g. 'https://localhost:8080'
        :param cert_path: e.g. '~/.lnd/tls.cert'
        :param macaroon_path: e.g. '~/.lnd/data/chain/bitcoin/testnet/admin.macaroon'
        """
        self._url = url + self.URL_SUFFIX
        self._cert_path = os.path.expanduser(cert_path)

        self._macaroon_path = os.path.expanduser(macaroon_path)
        with open(self._macaroon_path, 'rb') as f:
            macaroon = codecs.encode(f.read(), 'hex')
        self._headers = {'Grpc-Metadata-macaroon': macaroon}

    def get_url(self):
        return self._url[:-len(self.URL_SUFFIX)]

    def get_cert_path(self):
        return self._cert_path

    def get_macaroon_path(self):
        return self._macaroon_path

    def _get_request(self, action: str, **kwargs):
        """
        Sends a normal GET request
        :param action: Be appended to self.url
        :param kwargs: GET parameters
        :return:
        """
        try:
            response = requests.get(self._url + action, headers=self._headers, verify=self._cert_path, params=kwargs,
                                    timeout=self.TIMEOUT)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.ConnectionError as e:
            logger.warning('LND: raised ConnectionError: {}'.format(e.args))
            raise LndException(LndException.NOT_CONNECTED)

        except requests.exceptions.HTTPError as e:
            # if e.response.status_code == 404:
            #     return False
            logger.warning('LND: raised HTTPError: {}'.format(e.args))
            raise LndException(LndException.NOT_UNLOCKED)

    def _post_request(self, action: str, **kwargs):
        """
        Sends a POST request
        :param action: Be appended to self.url
        :param kwargs: POST data
        :return:
        """
        try:
            post_data = json.dumps(kwargs)
            response = requests.post(self._url + action, headers=self._headers, verify=self._cert_path,
                                     timeout=self.TIMEOUT, data=post_data)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.ConnectionError as e:
            logger.warning('LND: raised ConnectionError: {}'.format(e.args))
            raise LndException(LndException.NOT_CONNECTED)

        except requests.exceptions.HTTPError as e:
            # if e.response.status_code == 404:
            #     return False
            logger.warning('LND: raised HTTPError: {}'.format(e.args))
            raise LndException(LndException.NOT_UNLOCKED)

    def getinfo(self):
        return self._get_request('getinfo')

    def add_invoice(self, value: int, memo: str = None, **kwargs) -> (str, int, str):
        """
        :param value: Payment value in satoshis
        :param memo:
        :param kwargs: Other options
        :return: r_hash, add_index, payment_request
        """
        result = self._post_request('invoices', value=value, memo=memo, **kwargs)
        logger.info('LND: add_invoice: {}'.format(result))
        return result['r_hash'], int(result['add_index']), result['payment_request']

    def get_invoices(self, index_offset: int = None, num_max_invoices: int = None, reverse: bool = True, **kwargs)\
            -> (int, int, List[dict]):
        """
        :param index_offset:
        :param num_max_invoices:
        :param reverse:
        :param kwargs:
        :return: first_index_offset, last_index_offset, invoices
        """
        logger.debug('LND: get_invoices({}, {}, {})'.format(index_offset, num_max_invoices, reverse))
        invoices = self._get_request('invoices',
                                     index_offset=index_offset,
                                     num_max_invoices=num_max_invoices,
                                     reversed=reverse,
                                     **kwargs)
        # logger.debug('LND: invoices: {}'.format(invoices))
        """
        {
            'first_index_offset': '145', 
            'last_index_offset': '147',
            'invoices': [
                {
                    'payment_request': 'lntb257580n1pwyq42upp5s5el9cppvg44wy62x0wsdz2kmyrvnjtjy9xe0q427t0d5cc8sj6qd...', 
                    'add_index': '145', 
                    'expiry': '180', 
                    'r_preimage': 's+x8cV/wswrVdA342Mv3B5yNLXULaikZMxvuIzjPGwg=', 
                    'cltv_expiry': '144', 
                    'memo': 'description test', 
                    'creation_date': '1547720028', 
                    'r_hash': 'hTPy4CFiK1cTSjPdBolW2QbJyXIhTZeCqvLe2mMHhLQ=', 
                    'value': '25758'
                },
                {
                    ...
                    'amt_paid_msat': '25304000', 
                    'settle_index': '16', 
                    'settled': True,
                    'settle_date': '1547204924', 
                    'amt_paid': '25304000', 
                    'amt_paid_sat': '25304'
                    ...
                }
                ...
            ]
        }
        """
        if invoices and 'first_index_offset' in invoices and 'last_index_offset' in invoices and 'invoices' in invoices:
            return int(invoices['first_index_offset']), int(invoices['last_index_offset']), invoices['invoices']
        else:
            return None

    def get_invoice(self, r_hash: str):
        """
        :param r_hash: base64 string
        :return: invoice
        """
        r_hash_bytes = codecs.decode(r_hash.encode(), 'base64')
        r_hash_hex_bytes = codecs.encode(r_hash_bytes, 'hex')
        r_hash_hex_str = r_hash_hex_bytes.decode()
        invoice = self._get_request('invoice/' + r_hash_hex_str)
        return invoice

    def create_subscribe_invoices_thread(self, callback: Callable[[Response], None],
                                         add_index: int = None, settle_index: int = None) -> LndStreamThread:
        """
        :param callback:
            def callback(response: Response):
                for line in response.iter_lines():
                    json_data = json.loads(line.decode())
        :param add_index: If set, subscribe invoices from the position.
        :param settle_index: If set, subscribe invoices from the position.
        :return:
        """
        lnd_stream_thread = LndStreamThread(self._url, self._cert_path, self._headers,
                                            callback, add_index, settle_index)
        return lnd_stream_thread

    def unlock_wallet(self, wallet_password: str, **kwargs):
        """
        :param wallet_password:
        :param kwargs:
        :return:
        """

        def base64encode(text: str) -> str:
            """
            str => base64 str
            :param text:
            :return: base64 encoded string
            """
            return base64.b64encode(text.encode()).decode()

        wallet_password = base64encode(wallet_password)
        return self._post_request('unlockwallet', wallet_password=wallet_password, **kwargs)


class LndException(Exception):
    NOT_CONNECTED = 1
    NOT_UNLOCKED = 2

    def __init__(self, reason):
        """
        :param reason: NOT_CONNECTED, NOT_UNLOCKED
        """
        self.reason = reason

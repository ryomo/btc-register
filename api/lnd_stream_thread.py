import logging
import threading
from typing import Callable, Optional

import requests
from requests import Response

logger = logging.getLogger(__name__)


class LndStreamThread(threading.Thread):

    def __init__(self, url, cert_path, headers,
                 callback: Callable[[Response], None], add_index: int = None, settle_index: int = None):
        """
        :param url:
        :param cert_path:
        :param headers:
        :param callback:
            def callback(stream_response: Response):
                for raw_data in stream_response.iter_lines():
                    json_data = json.loads(raw_data.decode())
        :param add_index:
        :param settle_index:
        """
        super().__init__(daemon=True)
        self._url = url
        self._cert_path = cert_path
        self._headers = headers

        self._callback = callback  # type: Callable[[Response], None]
        self._add_index = add_index  # type: Optional[int]
        self._settle_index = settle_index  # type: Optional[int]
        self._message = None  # type: None|str

    def run(self):
        self.subscribe_invoices(self._callback, add_index=self._add_index, settle_index=self._settle_index)

    def subscribe_invoices(self, callback: Callable[[Response], None], **kwargs):
        try:
            # Should not set timeout here. http://docs.python-requests.org/en/master/user/quickstart/#timeouts
            with requests.get(self._url + 'invoices/subscribe', headers=self._headers, verify=self._cert_path,
                              params=kwargs, stream=True) as response:
                logger.info('LndStreamThread: Start subscribing invoices')
                if response.status_code != 200:
                    logger.error('LndStreamThread: response.status_code = {}'.format(response.status_code))
                    self._message = 'LND connection error'
                    return
                try:
                    callback(response)
                    logger.info('LndStreamThread: End subscribing invoices')
                except AttributeError:
                    import traceback
                    body = traceback.format_exc()
                    logger.warning('KNOWN ISSUE: ' + body)  # https://github.com/requests/requests/issues/3807
                    return
        except requests.exceptions.ConnectionError as e:
            logger.exception(e)
            self._message = 'LND connection failed'
            return
        except requests.exceptions.ReadTimeout as e:
            logger.exception(e)
            self._message = 'LND timeout'
            return

    def has_message(self):
        return bool(self._message)

    def pull_message(self):
        """
        Get a message, and delete it.
        :return:
        """
        message = self._message
        self._message = None
        return message

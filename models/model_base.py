import datetime
import logging

from kivy.app import App

from library.db import Db

logger = logging.getLogger(__name__)


class ModelBase:
    MAX_INTEGER = 9223372036854775807  # SQLite's max integer

    _db = App.get_running_app().db  # type: Db

    def __init__(self):
        self.id = None  # type: None|int
        self.created_at = None  # type: None|int
        self.updated_at = None  # type: None|int

    def set(self, columns: dict):
        """
        e.g.)
        payment.set({
            'method': PaymentMethod.LND,
            'amount': 300,  # In cents
        })
        :param columns:
        """
        for key, value in columns.items():
            if not hasattr(self, key):
                raise ModelException('Column[{}] not found'.format(key))
            setattr(self, key, value)

    @staticmethod
    def _get_timestamp_int():
        return int(datetime.datetime.now().timestamp())


class ModelException(Exception):
    pass

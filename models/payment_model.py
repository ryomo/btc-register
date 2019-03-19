import logging
import sqlite3
from enum import Enum
from typing import List

from library.db import Fetch
from models.model_base import ModelBase
from models.payment_btc_model import PaymentBtcModel
from models.payment_fiat_model import PaymentFiatModel

logger = logging.getLogger(__name__)


class PaymentMethod(Enum):
    # MIX = 1
    FIAT = 2
    LND = 3


class PaymentModel(ModelBase):
    """
    e.g.)
    payment = PaymentModel()
    payment.set({
        'method': PaymentMethod.LND,
        'amount': 300,  # In cents
    })
    if not payment.validate():
        self.message = self.app.messenger.error('Data is not valid.')
        logger.warning('PAYMENT: payment.__dict__ = {}'.format(payment.__dict__))
        return
    payment.create()
    """

    def __init__(self):
        super().__init__()
        self.method = None  # type: PaymentMethod  # Needs `self.method.value` to convert integer, when you save to db.
        self.amount = None  # type: int  # In cents, not in dollars.

    def validate(self):
        # amount
        if self.amount is None:
            return False
        elif self.amount > self.MAX_INTEGER:
            return False
        elif self.amount < 0:
            return False

        return True

    def create(self):
        self.created_at = self._get_timestamp_int()
        sql = (
            'INSERT INTO payment (method, amount, created_at)'
            ' VALUES (?, ?, ?)'
        )
        self._db.execute_simple(sql, (
            self.method.value,  # PaymentMethod -> int
            self.amount,
            self.created_at,
        ))

    def create_with_payment_fiat(self, payment_fiat: PaymentFiatModel):
        def callback(cursor):
            self.created_at = self._get_timestamp_int()
            sql1 = (
                'INSERT INTO payment (method, amount, created_at)'
                ' VALUES (?, ?, ?)'
            )
            params1 = (
                self.method.value,  # PaymentMethod -> int
                self.amount,
                self.created_at,
            )
            cursor.execute(sql1, params1)

            payment_fiat.payment_id = cursor.lastrowid
            payment_fiat.created_at = self._get_timestamp_int()
            sql2 = (
                'INSERT INTO payment_fiat (payment_id, paid, change, created_at)'
                ' VALUES (?, ?, ?, ?)'
            )
            params2 = (
                payment_fiat.payment_id,
                payment_fiat.paid,
                payment_fiat.change,
                payment_fiat.created_at
            )
            cursor.execute(sql2, params2)

        self._db.execute(callback)

    def create_with_payment_btc(self, payment_btc: PaymentBtcModel):
        def callback(cursor):
            self.created_at = self._get_timestamp_int()
            sql1 = (
                'INSERT INTO payment (method, amount, created_at)'
                ' VALUES (?, ?, ?)'
            )
            params1 = (
                self.method.value,  # PaymentMethod -> int
                self.amount,
                self.created_at,
            )
            cursor.execute(sql1, params1)

            payment_btc.payment_id = cursor.lastrowid
            payment_btc.created_at = self._get_timestamp_int()
            sql2 = (
                'INSERT INTO payment_btc (payment_id, satoshi, created_at)'
                ' VALUES (?, ?, ?)'
            )
            params2 = (
                payment_btc.payment_id,
                payment_btc.satoshi,
                payment_btc.created_at
            )
            cursor.execute(sql2, params2)

        self._db.execute(callback)

    def update(self):
        self.updated_at = self._get_timestamp_int()
        sql = (
            'UPDATE payment SET method = ?, amount = ?, updated_at = ? WHERE id = ?'
        )
        self._db.execute_simple(sql, (
            self.method.value,  # PaymentMethod -> int
            self.amount,
            self.updated_at,
            self.id,
        ))

    @classmethod
    def find_row(cls, payment_id) -> sqlite3.Row:
        """
        e.g.)
        row = PaymentModel.find_row(1)
        payment = PaymentModel()
        payment.set({
            'id': row['id'],
            'method': PaymentMethod(row['method']),
            'amount': row['amount'],
            'created_at': row['created_at'],
            'updated_at': row['updated_at'],
        })

        :param payment_id:
        :return:
        """
        sql = (
            # 'SELECT * FROM payment WHERE id = ?'
            ' SELECT '
            '  payment.id,'
            '  payment.method,'
            '  payment.amount,'
            '  payment.created_at,'
            '  payment.updated_at,'
            '  payment_btc.satoshi AS payment_btc_satoshi,'
            '  payment_fiat.paid AS payment_fiat_paid,'
            '  payment_fiat.change AS payment_fiat_change'
            ' FROM payment'
            ' LEFT JOIN payment_btc ON payment.id = payment_btc.payment_id'
            ' LEFT JOIN payment_fiat ON payment.id = payment_fiat.payment_id'
            ' WHERE payment.id = ?'
        )
        row = cls._db.execute_simple(sql, (payment_id,), fetch=Fetch.ONE)
        return row

    @classmethod
    def find_rows_for_pagination(cls, offset: int = None, max_rows: int = None, reverse: bool = True) -> List[sqlite3.Row]:
        """
        e.g.)
        payment_rows = PaymentModel.find_rows_for_pagination(0, 20, True)
        for payment_row in payment_rows:
            print(payment_row['payment_btc_satoshi'])

        :param offset:
        :param max_rows:
        :param reverse:
        :return:
        """
        sql = (
            ' SELECT'
            '  payment.id,'
            '  payment.method,'
            '  payment.amount,'
            '  payment.created_at,'
            '  payment.updated_at,'
            '  payment_btc.satoshi AS payment_btc_satoshi'
            ' FROM payment'
            ' LEFT JOIN payment_btc ON payment.id = payment_btc.payment_id'
            ' ORDER BY payment.created_at {} LIMIT ? OFFSET ?'
        ).format(
            'DESC' if reverse else 'ASC',
        )

        rows = cls._db.execute_simple(sql, (max_rows, offset), fetch=Fetch.ALL)
        for row in rows:
            logger.debug('PaymentModel: row.keys(): {}'.format(row.keys()))
        return rows

    @classmethod
    def count(cls):
        sql = (
            'SELECT COUNT(*) FROM payment'
        )
        row = cls._db.execute_simple(sql, fetch=Fetch.ONE)
        return row['COUNT(*)']

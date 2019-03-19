import logging
from decimal import Decimal

from kivy.app import App
from kivy.properties import StringProperty, ListProperty, BooleanProperty, NumericProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from library.fiat import Fiat
from library.utils import Utils
from controllers.main.main_screen_base import MainScreenBase
from models.payment_model import PaymentModel, PaymentMethod

logger = logging.getLogger(__name__)


# TODO: Add the function to calc daily and monthly sales.
class HistoryScreen(MainScreenBase):
    payments = ListProperty()  # type: list
    sort_reversed = BooleanProperty(True)  # type: bool

    PAGE_ITEM_NUM = 20

    def __init__(self, **kw):
        super().__init__(**kw)
        self.page_index = 0  # type: int
        self.page_index_max = 0  # type: int

    def on_enter(self, *args):
        super().on_enter(*args)
        self.move_page_first()

    def on_leave(self, *args):
        super().on_leave(*args)
        self.payments = []
        self.sort_reversed = True
        self.page_index = 0
        self.page_index_max = 0

    def _fetch_payments(self, offset: int):
        if offset < 0:
            offset = 0

        payment_rows = PaymentModel.find_rows_for_pagination(offset, self.PAGE_ITEM_NUM, self.sort_reversed)
        if not payment_rows:
            self.message = self.app.messenger.warning('Payment data not found.')
            return

        self.payments = []
        for payment_row in payment_rows:
            payment_btc_satoshi = payment_row['payment_btc_satoshi']
            self.payments.append({
                'payment_id': payment_row['id'],
                'method': PaymentMethod(payment_row['method']).name,
                'amount': payment_row['amount'],
                'created_at': Utils.timestamp_to_strftime(payment_row['created_at']),
                'btc': Utils.satoshi_to_btc(payment_btc_satoshi),
            })

        payment_count_all = PaymentModel.count()
        self.page_index_max = int(payment_count_all / self.PAGE_ITEM_NUM)

    def move_page_first(self):
        self._fetch_payments(0)

    def move_page_last(self):
        self.sort_reversed = not self.sort_reversed
        self.move_page_first()
        self.sort_reversed = not self.sort_reversed
        self.payments.reverse()

    def move_page_next(self):
        if self.page_index < self.page_index_max:
            self.page_index += 1

        self._fetch_payments(self.PAGE_ITEM_NUM * self.page_index)

    def move_page_prev(self):
        if self.page_index > 0:
            self.page_index -= 1

        self._fetch_payments(self.PAGE_ITEM_NUM * self.page_index)

    def reload_page(self):
        self._fetch_payments(self.PAGE_ITEM_NUM * self.page_index)

    def reverse_sort(self):
        self.sort_reversed = not self.sort_reversed
        self.move_page_first()

    def popup(self, payment_id):
        """
        Open PaymentDetailPopup view.
        :param payment_id:
        :return:
        """
        payment_row = PaymentModel.find_row(payment_id)
        PaymentDetailPopup().open(payment_row)


class PaymentHistoryRow(BoxLayout, Button):
    payment_id = NumericProperty()
    method = StringProperty()
    amount = NumericProperty()
    created_at = StringProperty()
    btc = ObjectProperty(Decimal(), allownone=True)


class PaymentDetailPopup(Popup):

    def open(self, *largs, **kwargs):
        payment_row = largs[0]
        logger.debug('PaymentDetailPopup: payment_row = {}'.format(payment_row))

        def add_row(key: str, text: str):
            self.ids.container.add_widget(PaymentDetailRow(
                title=key,
                text=text,
            ))

        fiat = App.get_running_app().fiat  # type: Fiat
        payment_method = PaymentMethod(payment_row['method'])
        payment_date = Utils.timestamp_to_strftime(payment_row['created_at'])
        payment_btc_satoshi = payment_row['payment_btc_satoshi']

        self.title = '[{}] ({})'.format(payment_method.name, payment_date)

        add_row('ID', '{:,}'.format(payment_row['id']))
        add_row('Date', payment_date)
        add_row('Method', payment_method.name)
        if payment_method == PaymentMethod.FIAT:
            add_row('Total', '{} {:,}'.format(fiat.mark, payment_row['amount']))
            add_row('Paid', '{} {:,}'.format(fiat.mark, payment_row['payment_fiat_paid']))
            add_row('Change', '{} {:,}'.format(fiat.mark, payment_row['payment_fiat_change']))
        elif payment_method == PaymentMethod.LND:
            add_row('Amount', '{} {:,}'.format(fiat.mark, payment_row['amount']))
            add_row('BTC', '{:,} BTC'.format(Utils.satoshi_to_btc(payment_btc_satoshi)))
        else:
            raise ValueError

        super().open(*largs, **kwargs)


class PaymentDetailRow(BoxLayout):
    title = StringProperty()
    text = StringProperty()

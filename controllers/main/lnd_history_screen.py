import logging

from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from api.lnd import LndException
from library.utils import Utils
from controllers.main.main_screen_base import MainScreenBase

logger = logging.getLogger(__name__)


# TODO: This screen may not require anymore.
# TODO: Check if the wallet is unlocked.
class LndHistoryScreen(MainScreenBase):
    invoices = ListProperty()
    sort_reversed = BooleanProperty(True)

    PAGE_ITEM_NUM = 20

    def __init__(self, **kw):
        super().__init__(**kw)
        self.first_index_offset = None  # type: int
        self.last_index_offset = None  # type: int

    def on_enter(self, *args):
        super().on_enter(*args)
        self.move_page_first()

    def on_leave(self, *args):
        super().on_leave(*args)
        self.invoices = []
        self.sort_reversed = True
        self.first_index_offset = None
        self.last_index_offset = None

    def _fetch_invoices(self, index_offset: int):
        if index_offset < 0:
            index_offset = 0

        try:
            index_and_invoices = self.app.lnd.get_invoices(index_offset, 20, self.sort_reversed)
        except LndException as e:
            logger.warning(e.args)
            self.message = self.app.messenger.warning('Unable to load invoices from LND.')
            return

        if not index_and_invoices:
            self.message = self.app.messenger.warning('Invoice not found.')
            return
        self.first_index_offset, self.last_index_offset, tmp_invoices = index_and_invoices

        if self.sort_reversed:
            tmp_invoices.reverse()

        self.invoices = []
        for invoice in tmp_invoices:
            self.invoices.append({
                'r_hash': invoice['r_hash'],
                'add_index': '{:,}'.format(int(invoice['add_index'])),
                'memo': Utils.sanitize(invoice['memo']) if 'memo' in invoice else '-',
                'satoshi': '{:,}'.format(int(invoice['value'])) if 'value' in invoice else '-',
                'creation_date': Utils.timestamp_to_strftime(invoice['creation_date']),
                'settled': '✓' if ('settled' in invoice and invoice['settled']) else '-',
            })

    def move_page_first(self):
        self._fetch_invoices(0)

    def move_page_last(self):
        self.sort_reversed = not self.sort_reversed
        self.move_page_first()
        self.sort_reversed = not self.sort_reversed
        self.invoices.reverse()

    def move_page_next(self):
        if self.sort_reversed:
            self._fetch_invoices(self.first_index_offset)
        else:
            self._fetch_invoices(self.last_index_offset)

    def move_page_prev(self):
        if self.sort_reversed:
            self._fetch_invoices(self.last_index_offset + self.PAGE_ITEM_NUM + 1)
        else:
            self._fetch_invoices(self.first_index_offset - self.PAGE_ITEM_NUM - 1)

    def reload_page(self):
        if self.sort_reversed:
            self._fetch_invoices(self.last_index_offset + 1)
        else:
            self._fetch_invoices(self.first_index_offset - 1)

    def reverse_sort(self):
        self.sort_reversed = not self.sort_reversed
        self.move_page_first()

    def popup(self, r_hash):
        """
        Open LndDetailPopup view.
        :param r_hash:
        :return:
        """
        invoice = self.app.lnd.get_invoice(r_hash)
        LndDetailPopup().open(invoice)


class LndHistoryRow(BoxLayout, Button):
    r_hash = StringProperty('')
    add_index = StringProperty('')
    memo = StringProperty('')
    satoshi = StringProperty('')
    creation_date = StringProperty('')
    settled = StringProperty('')


class LndDetailPopup(Popup):

    def open(self, *largs, **kwargs):
        invoice = largs[0]
        logger.debug('LndDetailPopup: invoice = {}'.format(invoice))

        def add_row(_invoice, _key, text_if_exist=None, text_if_not_exist='-'):
            if _key in _invoice:
                self.ids.container.add_widget(LndDetailRow(
                    title=_key,
                    text=text_if_exist if text_if_exist else Utils.sanitize(_invoice[_key]),
                ))
            else:
                self.ids.container.add_widget(LndDetailRow(
                    title=_key,
                    text=text_if_not_exist
                ))

        self.title = '[{}]'.format(invoice['add_index'])

        add_row(invoice, 'add_index')
        add_row(invoice, 'r_hash')
        add_row(invoice, 'memo')
        add_row(invoice, 'creation_date', Utils.timestamp_to_strftime(invoice['creation_date']))
        add_row(invoice, 'settled', '✓')
        add_row(invoice, 'settle_date',
                Utils.timestamp_to_strftime(invoice['settle_date']) if 'settle_date' in invoice else None)
        add_row(invoice, 'amt_paid_msat')
        add_row(invoice, 'amt_paid_sat')
        add_row(invoice, 'fallback_addr')

        """
        fallback_addr	string	/ Fallback on-chain address.
        r_hash	byte	/ The hash of the preimage
        settle_date	string	/ When this invoice was settled
        expiry	string	/ Payment request expiry time in seconds. Default is 3600 (1 hour).
        memo	string	* An optional memo to attach along with the invoice. Used for record keeping purposes for the invoice’s creator, and will also be set in the description field of the encoded payment request if the description_hash field is not being used.
        receipt	byte	/ An optional cryptographic receipt of payment
        settle_index	string	* The “settle” index of this invoice. Each newly settled invoice will increment this index making it monotonically increasing. Callers to the SubscribeInvoices call can use this to instantly get notified of all settled invoices with an settle_index greater than this one.
        add_index	string	* The “add” index of this invoice. Each newly created invoice will increment this index making it monotonically increasing. Callers to the SubscribeInvoices call can use this to instantly get notified of all added invoices with an add_index greater than this one.
        payment_request	string	* A bare-bones invoice for a payment within the Lightning Network. With the details of the invoice, the sender has all the data necessary to send a payment to the recipient.
        value	string	/ The value of this invoice in satoshis
        settled	boolean	/ Whether this invoice has been fulfilled
        amt_paid_msat	string	* The amount that was accepted for this invoice, in millisatoshis. This will ONLY be set if this invoice has been settled. We provide this field as if the invoice was created with a zero value, then we need to record what amount was ultimately accepted. Additionally, it’s possible that the sender paid MORE that was specified in the original invoice. So we’ll record that here as well.
        amt_paid	string	/ Deprecated, use amt_paid_sat or amt_paid_msat.
        amt_paid_sat	string	* The amount that was accepted for this invoice, in satoshis. This will ONLY be set if this invoice has been settled. We provide this field as if the invoice was created with a zero value, then we need to record what amount was ultimately accepted. Additionally, it’s possible that the sender paid MORE that was specified in the original invoice. So we’ll record that here as well.
        private	boolean	/ Whether this invoice should include routing hints for private channels.
        creation_date	string	/ When this invoice was created
        description_hash	byte	* Hash (SHA-256) of a description of the payment. Used if the description of payment (memo) is too long to naturally fit within the description field of an encoded payment request.
        r_preimage	byte	* The hex-encoded preimage (32 byte) which will allow settling an incoming HTLC payable to this preimage
        cltv_expiry	string	/ Delta to use for the time-lock of the CLTV extended to the final hop.
        """

        super().open(*largs, **kwargs)


class LndDetailRow(BoxLayout):
    title = StringProperty()
    text = StringProperty()

import json
import logging

from kivy.core.image import Image as CoreImage
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from requests import Response

from api.lnd_stream_thread import LndStreamThread
from controllers.main.main_screen_base import MainScreenBase
from controllers.partials.qr_code import QrCode
from library.utils import Utils
from models.payment_btc_model import PaymentBtcModel
from models.payment_model import PaymentModel, PaymentMethod

logger = logging.getLogger(__name__)


class WaitLndScreen(MainScreenBase):
    btcprice_fixed = NumericProperty(0)  # type: int  # In cents
    btcprice_date_fixed = StringProperty()  # YYYY/MM/DD

    payment_satoshi = NumericProperty(0)  # type: int  # In satoshis
    payment_amount = NumericProperty(0)  # type: int  # In cents

    qrcode_texture = ObjectProperty(None, allownone=True)
    result_texture = ObjectProperty(None, allownone=True)
    result_texture_alpha = NumericProperty(0)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.lnd_subscribe_invoices_thread = ...  # type: LndStreamThread
        self.is_payment_confirmed = False

    def on_enter(self, *args):
        super().on_enter(*args)

        self.schedule_interval(self.update, 1 / 30)

        invoice = self.manager.get_interscreen_data('invoice')
        r_hash = invoice[0]
        add_index = invoice[1]
        payment_request = invoice[2]
        self.btcprice_fixed = invoice[3]
        self.btcprice_date_fixed = invoice[4]
        self.payment_satoshi = invoice[5]
        self.payment_amount = invoice[6]

        # QR code
        img_data = Utils.generate_qrcode(payment_request)
        self.qrcode_texture = CoreImage(img_data, ext='png').texture

        def callback(response: Response):
            for line in response.iter_lines():  # Note: iter_lines() is a blocking method
                json_data = json.loads(line.decode())
                result = json_data['result']
                if 'settled' in result and result['settled'] and result['r_hash'] == r_hash:
                    logger.info('WaitPaymentScreen: Payment confirmed')
                    self.is_payment_confirmed = True

                    # Saves to DB
                    # payment
                    payment = PaymentModel()
                    payment.set({
                        'method': PaymentMethod.LND,
                        'amount': self.payment_amount,
                    })
                    # payment btc
                    payment_btc = PaymentBtcModel()
                    payment_btc.set({
                        'satoshi': self.payment_satoshi,
                    })
                    # validate
                    if not payment.validate() or not payment_btc.validate():
                        self.message = self.app.messenger.error('Invalid payment.')
                        logger.warning('PAYMENT LND: payment.__dict__ = {}'.format(payment.__dict__))
                        logger.warning('PAYMENT LND: payment_btc.__dict__ = {}'.format(payment_btc.__dict__))
                        return
                    # create
                    payment.create_with_payment_btc(payment_btc)

                    return

        self.lnd_subscribe_invoices_thread = self.app.lnd.create_subscribe_invoices_thread(callback, add_index - 1)
        self.lnd_subscribe_invoices_thread.start()

    def on_leave(self, *args):
        super().on_leave(*args)

        self.btcprice_fixed = 0
        self.btcprice_date_fixed = ''
        self.payment_satoshi = 0
        self.payment_amount = 0

        self.qrcode_texture = None
        self.result_texture = None
        self.result_texture_alpha = 0

        self.app.send_data_to_subproc('screen', 'idle')

    def update(self, dt):
        if self.lnd_subscribe_invoices_thread.has_message():
            self.message = self.lnd_subscribe_invoices_thread.pull_message()

        if self.is_payment_confirmed and not self.result_texture:
            self.result_texture = CoreImage('assets/success.png').texture
            self.result_texture_alpha = 1
            self.app.send_data_to_subproc('settled', True)

    def back_to_input_screen(self):
        self.manager.transition.direction = 'right'

        if self.is_payment_confirmed:
            self.manager.set_interscreen_data('clear_inputted_data', True)
            self.manager.load_screen('home')
        else:
            self.manager.load_screen('home')


class QrCodeMain(QrCode):
    pass

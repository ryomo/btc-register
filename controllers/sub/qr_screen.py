import logging

from kivy.core.image import Image as CoreImage
from kivy.properties import NumericProperty, ObjectProperty, StringProperty

from controllers.partials.qr_code import QrCode
from controllers.sub.sub_screen_base import SubScreenBase
from library.utils import Utils

logger = logging.getLogger(__name__)


class QrScreen(SubScreenBase):
    btcprice_fixed = NumericProperty(0)  # type: int  # In cents
    btcprice_time_fixed = StringProperty()  # HH:MM

    payment_satoshi = NumericProperty(0)  # type: int  # In satoshis
    payment_amount = NumericProperty(0)  # type: int  # In cents

    qrcode_texture = ObjectProperty(None, allownone=True)
    result_texture = ObjectProperty(None, allownone=True)
    result_texture_alpha = NumericProperty(0)

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.schedule_interval(self.update, 1 / 30)

    def on_leave(self, *args):
        super().on_leave(*args)

        self.btcprice_fixed = 0
        self.btcprice_time_fixed = ''
        self.payment_satoshi = 0
        self.payment_amount = 0

        self.qrcode_texture = None
        self.result_texture = None
        self.result_texture_alpha = 0

    def update(self, dt=None):
        payment_data = self.app.receive_data_from_mainproc('payment')
        if payment_data:
            self.btcprice_fixed = payment_data[0]
            self.btcprice_time_fixed = payment_data[1]
            self.payment_satoshi = payment_data[2]
            self.payment_amount = payment_data[3]
            payment_request = payment_data[4]

            # QR code
            img_data = Utils.generate_qrcode(payment_request)
            self.qrcode_texture = CoreImage(img_data, ext='png').texture

        settled = self.app.receive_data_from_mainproc('settled')
        if settled:
            self.result_texture = CoreImage('assets/success.png').texture
            self.result_texture_alpha = 1


class QrCodeSub(QrCode):
    pass

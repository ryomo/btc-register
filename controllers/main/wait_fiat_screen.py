import logging

from kivy.properties import NumericProperty

from controllers.main.main_screen_base import MainScreenBase
from controllers.partials.numpad import NumPad
from models.payment_fiat_model import PaymentFiatModel
from models.payment_model import PaymentModel, PaymentMethod

logger = logging.getLogger(__name__)


class WaitFiatScreen(MainScreenBase):
    payment_total = NumericProperty(0)  # type: int  # In cents
    payment_paid = NumericProperty(0)  # type: int  # In cents
    payment_change = NumericProperty(0)  # type: int  # In cents

    def on_enter(self, *args):
        super().on_enter(*args)
        self.payment_total = self.manager.get_interscreen_data('payment_fiat')

    def on_leave(self, *args):
        super().on_leave(*args)
        self.payment_total = 0
        self.payment_paid = 0
        self.payment_change = 0
        self.ids.numpad.number_display = ''
        self.app.send_data_to_subproc('screen', 'idle')

    def back_to_input_screen(self):
        self.manager.transition.direction = 'right'
        self.manager.load_screen('home')

    def push_done_button(self):
        # Saves to DB
        # payment
        payment = PaymentModel()
        payment.set({
            'method': PaymentMethod.FIAT,
            'amount': self.payment_total,
        })
        # payment btc
        payment_fiat = PaymentFiatModel()
        payment_fiat.set({
            'paid': self.payment_paid,
            'change': self.payment_change,
        })
        # validate
        if not payment.validate() or not payment_fiat.validate():
            self.message = self.app.messenger.error('invalid_payment_fiat')
            logger.warning('PAYMENT FIAT: payment.__dict__ = {}'.format(payment.__dict__))
            logger.warning('PAYMENT FIAT: payment_fiat.__dict__ = {}'.format(payment_fiat.__dict__))
            return
        # create
        payment.create_with_payment_fiat(payment_fiat)

        self.manager.set_interscreen_data('clear_inputted_data', True)
        self.manager.load_screen('home')


class NumPadChange(NumPad):

    def push_image_button(self):
        """
        Calculates change
        """
        number_display = self.number_display.rstrip('.')  # type: str  # In dollars

        if not number_display:
            self.screen.message = self.app.messenger.warning('amount_not_inputted')
            return

        self.screen.payment_paid = self.app.fiat.dollar_str_to_cent(number_display)
        self.screen.payment_change = self.screen.payment_paid - self.screen.payment_total

        self.app.send_data_to_subproc('payment_change_info', (
            self.screen.payment_total,
            self.screen.payment_paid,
            self.screen.payment_change
        ))

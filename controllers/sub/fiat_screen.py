import logging

from kivy.properties import NumericProperty

from controllers.sub.sub_screen_base import SubScreenBase

logger = logging.getLogger(__name__)


class FiatScreen(SubScreenBase):
    payment_total = NumericProperty(0)  # type: int  # In cents
    payment_paid = NumericProperty(0)  # type: int  # In cents
    payment_change = NumericProperty(0)  # type: int  # In cents

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.schedule_interval(self.update, 1 / 30)

    def on_leave(self, *args):
        super().on_leave(*args)
        self.payment_total = 0
        self.payment_paid = 0
        self.payment_change = 0

    def update(self, dt):
        payment_total = self.app.receive_data_from_mainproc('payment_fiat')
        if payment_total:
            self.payment_total = payment_total

        payment_change_info = self.app.receive_data_from_mainproc('payment_change_info')
        if payment_change_info:
            self.payment_total = payment_change_info[0]
            self.payment_paid = payment_change_info[1]
            self.payment_change = payment_change_info[2]

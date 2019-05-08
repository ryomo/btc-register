import logging

from kivy.properties import StringProperty, NumericProperty

from controllers.sub.sub_screen_base import SubScreenBase

logger = logging.getLogger(__name__)


class IdleScreen(SubScreenBase):
    # btcprice and btcprice_time are updated by SubApp.update_btcdata().
    btcprice = NumericProperty(0)  # type: int  # In cents
    btcprice_time = StringProperty()  # HH:MM

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.btcprice = self.app.btcprice
        self.btcprice_time = self.app.btcprice_time

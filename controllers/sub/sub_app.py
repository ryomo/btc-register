import logging
import time
from threading import Thread
from typing import Any, Optional

from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import NoTransition

from controllers.app_base import AppBase
from controllers.sub.sub_screen_manager import SubScreenManager
from library.config import Config
from run import APP_PATH

DEBUG_SCREEN = None
# DEBUG_SCREEN = 'fiat'

logger = logging.getLogger(__name__)


class SubApp(AppBase):
    kv_file = APP_PATH + '/views/sub/sub.kv'

    btcprice = NumericProperty(0)  # type: int  # In cents
    btcprice_time = StringProperty()  # HH:MM

    def __init__(self, pipe, app_config: Config, **kwargs):
        super().__init__(pipe, app_config, **kwargs)

        self._pipe = pipe
        self._piped_data = None  # type: Optional[(str, Any)]  # Data sent from the main process.

        self.screen_manager = ...  # type: SubScreenManager

    def build(self):
        super().build()

        def receive_pipe(_pipe):
            while True:
                # Ensure `_piped_data` is empty.
                if self._piped_data:
                    time.sleep(0.1)
                    continue
                self._piped_data = _pipe.recv()  # Note: pipe.recv() is a blocking method.
                logger.debug('PIPE: {}'.format(self._piped_data))

        thread = Thread(target=receive_pipe, args=(self._pipe,))
        thread.start()

        Clock.schedule_interval(self.update_btcdata, 1 / 30)

        self.screen_manager = SubScreenManager(self._pipe, transition=NoTransition())

        if DEBUG_SCREEN:
            self.screen_manager.load_screen(DEBUG_SCREEN)
        else:
            self.screen_manager.load_screen('idle')

        return self.screen_manager

    def update_btcdata(self, dt):
        btcdata = self.receive_data_from_mainproc('btcdata')
        if btcdata:
            self.btcprice = btcdata[0]
            self.btcprice_time = btcdata[1]

            # Updates screen's btcprice and btcprice_time.
            if hasattr(self.screen_manager.current_screen, 'btcprice'):
                self.screen_manager.current_screen.btcprice = self.btcprice
            if hasattr(self.screen_manager.current_screen, 'btcprice_time'):
                self.screen_manager.current_screen.btcprice_time = self.btcprice_time

    def receive_data_from_mainproc(self, key):
        """
        Gets data sent by send_data_to_subproc() from main process.
        (e.g.)
        self.manager.send_data_to_subproc('btc_price', price)
        ...
        btc_price = self.manager.receive_data_from_mainproc('btc_price')
        :param key:
        :return:
        """
        if self._piped_data and self._piped_data[0] == key:
            tmp_piped_data = self._piped_data[1]
            self._piped_data = None
            return tmp_piped_data
        else:
            return None

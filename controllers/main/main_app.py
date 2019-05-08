import locale
import logging
from decimal import Decimal

import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import BooleanProperty, StringProperty, NumericProperty

from api.lnd import Lnd, LndException
from controllers.main.main_screen_manager import MainScreenManager
from library.config import Config
from library.db import Db
from localize.digit import Digit
from library.exchange import Exchange, ExchangeEnum, ExchangeException
from localize.fiat import Fiat
from library.utils import Utils
from localize.messenger import Messenger
from run import APP_PATH, APP_HOME

kivy.require('1.10.0')

DEBUG_SCREEN = None
# DEBUG_SCREEN = 'history'

logger = logging.getLogger(__name__)

locale.setlocale(locale.LC_ALL, '')


class MainApp(App):
    kv_file = APP_PATH + '/views/main/main.kv'

    btcprice = NumericProperty(0)  # type: int  # In cents
    btcprice_time = StringProperty()  # HH:MM

    enable_update_btcdata = BooleanProperty(True)  # type: BooleanProperty

    def __init__(self, pipe, app_config: Config, **kwargs):
        super().__init__(**kwargs)
        self._pipe = pipe  # Inter process connection to send some data.

        self.screen_manager = ...  # type: MainScreenManager
        self.app_config = app_config  # type: Config
        self.db = ...  # type: Db
        self.lnd = ...  # type: Lnd
        self.messenger = ...  # type: Messenger
        self.m = ...  # type: Messenger.get_text  # Usage: app.m('key')
        self.exchange = ...  # type: Exchange
        self.fiat = ...  # type: Fiat
        self.digit = ...  # type: Digit

    def build(self):
        db_path = APP_HOME + '/database.db'
        self.db = Db(db_path, APP_PATH + '/schemas/')

        c = self.app_config
        logger.debug('APP CONFIG: []'.format(self.app_config))
        if c.get('lnd', 'url') and c.get('lnd', 'cert_path') and c.get('lnd', 'macaroon_path'):
            try:
                self.lnd = Lnd(c.get('lnd', 'url'), c.get('lnd', 'cert_path'), c.get('lnd', 'macaroon_path'))
            except LndException as e:
                if e.reason == LndException.FILE_NOT_FOUND:
                    self.lnd = None
                    logger.warning('LND: {}'.format(e.message))
                else:
                    raise e
        else:
            self.lnd = None

        self.messenger = Messenger(self.app_config.get('app', 'lang'))
        self.m = self.messenger.get_text

        self.fiat = Fiat(self.app_config.get('app', 'fiat'))
        self.digit = Digit()

        exchange_enum = ExchangeEnum(self.app_config.get('btc', 'price'))  # type: ExchangeEnum
        self.exchange = Exchange(exchange_enum)

        Clock.schedule_once(self.update_btcdata)
        Clock.schedule_interval(self.update_btcdata, 60)

        self.screen_manager = MainScreenManager()

        if DEBUG_SCREEN:
            # noinspection PyTypeChecker
            self.load_debug_screen(DEBUG_SCREEN)
        else:
            self.screen_manager.load_screen('home')

        return self.screen_manager

    def load_debug_screen(self, screen_name: str):
        if screen_name == 'wait_lnd':
            payment_request = 'lntb249790n1pwztadvpp5cefc0cac0fnc3n39p7n9rmh9msgqd854ln879e6wvp54f6jzc...'
            self.screen_manager.set_interscreen_data('invoice', (
                'xlOH47h6Z4jOJQ+mUe7l3BAGnpX8z+LnTmBpVOpCxjA=',
                103,  # settled
                # 1000000,  # not settled
                payment_request, 390000, '2019/03/13', 100000, 390
            ))
            self.send_data_to_subproc('screen', 'qr')
            self.send_data_to_subproc('payment',
                                      (390000, '14:23', 100000, 390, payment_request))

        elif screen_name == 'wait_fiat':
            payment_fiat = 1500
            self.send_data_to_subproc('screen', 'fiat')
            self.send_data_to_subproc('payment_fiat', payment_fiat)
            self.screen_manager.transition.direction = 'left'
            self.screen_manager.set_interscreen_data('payment_fiat', payment_fiat)
            self.screen_manager.load_screen('wait_fiat')

        self.screen_manager.load_screen(screen_name)

    def update_btcdata(self, dt=None):
        if not self.enable_update_btcdata:
            return
        try:
            self.btcprice = self.exchange.fetch_btc_price()
            self.btcprice_time = Utils.get_strftime('%H:%M')

            self.send_data_to_subproc('btcdata', (self.btcprice, self.btcprice_time))

            # Updates screen's btcprice and btcprice_time.
            if hasattr(self.screen_manager.current_screen, 'btcprice'):
                self.screen_manager.current_screen.btcprice = self.btcprice
            if hasattr(self.screen_manager.current_screen, 'btcprice_time'):
                self.screen_manager.current_screen.btcprice_time = self.btcprice_time

        except ExchangeException as e:
            logger.exception(e)
            self.screen_manager.current_screen.message = self.messenger.error('Network error')

    def on_enable_update_btcdata(self, instance, enable_update_btcdata):
        logger.info('MAIN: enable_update_btcdata: {}'.format(self.enable_update_btcdata))
        if self.enable_update_btcdata:
            self.update_btcdata()

    def send_data_to_subproc(self, key: str, value):
        """
        Sends some data to the sub process.
        (e.g.)
        self.app.send_data_to_subproc('btc_price', price)
        ...
        btc_price = self.app.receive_data_from_mainproc('btc_price')
        :param key:
        :param value:
        """
        self._pipe.send((key, value))

    def restart(self):
        """
        Restarts this app. See `run.sh`.
        """
        open(APP_HOME + '/.restart', 'w').close()
        self.stop()

    def shutdown(self):
        """
        Exit this app and shutdown Raspberry Pi. See `run.sh`.
        """
        open(APP_HOME + '/.shutdown', 'w').close()
        self.stop()

    def f(self, number: Decimal) -> str:
        """
        Format fiat currency.
        e.g.) '$ 123.45'
        :param number:
        :return:
        """
        if number == 0:
            return '0'
        return self.fiat.symbol + ' ' + self.digit.format(number, self.fiat.frac_digits)

    def c(self, number: Decimal) -> str:
        """
        Format crypto currency.
        E.g.) '0.00001234'
        :param number:
        :return:
        """
        if number == 0:
            return '0'
        return self.digit.format(number, 8)

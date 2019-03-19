import logging

from kivy.properties import ListProperty, StringProperty

from controllers.main.main_screen_base import MainScreenBase
from library.exchange import ExchangeEnum

logger = logging.getLogger(__name__)


class SettingScreen(MainScreenBase):
    exchanges = ListProperty()
    shop_name = StringProperty()
    lnd_url = StringProperty()
    lnd_cert_path = StringProperty()
    lnd_macaroon_path = StringProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.selected_exchange_name = None  # str

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)

        self.exchanges = ExchangeEnum.get_value_list()  # e.g. ['GDAX(USD)', 'bitFlyer(JPY)']

        # exchange
        exchange_enum = self.app.exchange.get_exchange_enum()
        self.exchange_spinner.text = exchange_enum.value

        self.shop_name = self.app.app_config.get('shop', 'name')
        self.lnd_url = self.app.app_config.get('lnd', 'url')
        self.lnd_cert_path = self.app.app_config.get('lnd', 'cert_path')
        self.lnd_macaroon_path = self.app.app_config.get('lnd', 'macaroon_path')

    def select_exchange_spinner(self, spinner_text):
        self.selected_exchange_name = spinner_text

    def save_and_restart(self):
        if self.selected_exchange_name:
            exchange_enum = ExchangeEnum(self.selected_exchange_name)
            self.app.app_config.set('btc', 'price', self.selected_exchange_name)
            fiat_name = exchange_enum.get_fiat_name()
            self.app.app_config.set('fiat', 'name', fiat_name)

        self.app.app_config.set('shop', 'name', self.shop_name)

        self.app.app_config.set('lnd', 'url', self.lnd_url)
        self.app.app_config.set('lnd', 'cert_path', self.lnd_cert_path)
        self.app.app_config.set('lnd', 'macaroon_path', self.lnd_macaroon_path)

        self.app.app_config.write()

        self.app.restart()

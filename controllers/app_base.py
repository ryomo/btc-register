import locale
import logging
from decimal import Decimal

from kivy.app import App

from library.config import Config
from localize.digit import Digit
from localize.fiat import Fiat
from localize.messenger import Messenger

logger = logging.getLogger(__name__)

locale.setlocale(locale.LC_ALL, '')


class AppBase(App):

    def __init__(self, pipe, app_config: Config, **kwargs):
        super().__init__(**kwargs)

        self.app_config = app_config  # type: Config
        self.messenger = ...  # type: Messenger
        self.fiat = ...  # type: Fiat
        self.digit = ...  # type: Digit

    def build(self):
        self.messenger = Messenger(self.app_config.get('app', 'lang'))
        self.fiat = Fiat(self.app_config.get('app', 'fiat'))
        self.digit = Digit()

    def m(self, message_key: str):
        """
        Return localized message.
        Usage: app.m('key')
        :param message_key:
        :return:
        """
        return self.messenger.get_text(message_key)

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

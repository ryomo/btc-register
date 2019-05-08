import locale
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)


class Digit:
    """
    Localize number formats.
    Note: Need `locale.setlocale(locale.LC_ALL, '')` before instantiate this class.
    """

    def __init__(self):
        self._localeconv = locale.localeconv()  # https://docs.python.org/3/library/locale.html#locale.localeconv
        logger.debug('LOCALE: {}'.format(locale.getlocale()))

    @staticmethod
    def format(number: Decimal, flac_digit: int = 0) -> str:
        return locale.format_string('%.{}f'.format(flac_digit), number, grouping=True)

    def get_decimal_point(self) -> str:
        return self._localeconv['mon_decimal_point']

import datetime
import decimal
import io
import logging
from decimal import Decimal
from typing import Optional

logger = logging.getLogger(__name__)


class Utils:

    @staticmethod
    def change_backlight_state(enable_backlight: bool = True):
        """
        Turns backlight on.
        Note: The bl_power file needs to be writable. `sudo chmod a+w /sys/class/backlight/rpi_backlight/bl_power`
        :param enable_backlight:
        :return: Returns True if backlight is on, False if it is off. Returns None if error occured.
        """
        import subprocess
        try:
            bl_power = 0 if enable_backlight else 1
            subprocess.check_call('echo {} > /sys/class/backlight/rpi_backlight/bl_power'.format(bl_power), shell=True)
            return enable_backlight
        except subprocess.CalledProcessError as e:
            logger.exception(e)
            return None

    @staticmethod
    def timestamp_to_strftime(timestamp, datetime_format='%Y/%m/%d %H:%M') -> str:
        if not timestamp:
            return ''
        dt = datetime.datetime.fromtimestamp(float(timestamp))
        return dt.strftime(datetime_format)

    @staticmethod
    def get_strftime(datetime_format='%Y/%m/%d %H:%M'):
        return datetime.datetime.now().strftime(datetime_format)

    @staticmethod
    def sanitize(text):
        """
        Use this before showing text on views
        :param text:
        :return:
        """
        text = str(text)\
            .replace('\n', '\\n')\
            .replace('\r', '\\r')
        return text

    @staticmethod
    def snake_to_camel(text: str):
        """
        snake_case -> CamelCase
        :param text:
        :return:
        """
        words = text.split('_')
        words = map(lambda x: x.capitalize(), words)
        return ''.join(words)

    @staticmethod
    def generate_qrcode(text: str):
        import qrcode
        img_io = io.BytesIO()
        qr = qrcode.make(text)
        qr.save(img_io, ext='png')
        img_io.seek(0)
        img_data = io.BytesIO(img_io.read())
        return img_data

    @staticmethod
    def satoshi_to_btc(satoshi: Optional[int]) -> Optional[Decimal]:
        if satoshi is None:
            return None
        if satoshi == 0:
            return Decimal(0)
        return (Decimal(satoshi) / 100000000).quantize(Decimal('0.00000001'))

    @staticmethod
    def fiat_to_satoshi(fiat: int, btcprice: int) -> int:
        """
        :param fiat: In cents
        :param btcprice: In cents
        :return: satoshi
        """
        satoshi = Decimal(fiat) / Decimal(btcprice) * 100000000
        satoshi = satoshi.quantize(
            Decimal('1'),
            rounding=decimal.ROUND_HALF_UP
        )
        return int(satoshi)

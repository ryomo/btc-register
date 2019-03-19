from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout


class QrCode(BoxLayout):
    btcprice_fixed = NumericProperty(0)  # type: int  # In cents
    btcprice_date_fixed = StringProperty()  # YYYY/MM/DD

    payment_satoshi = NumericProperty(0)  # type: int  # In satoshis
    payment_amount = NumericProperty(0)  # type: int  # In cents

    qrcode_texture = ObjectProperty(None, allownone=True)
    result_texture = ObjectProperty(None, allownone=True)
    result_texture_alpha = NumericProperty(0)

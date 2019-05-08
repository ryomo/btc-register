import logging
from decimal import Decimal

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivy.uix.widget import Widget

from api.lnd import LndException
from controllers.main.main_app import MainApp
from controllers.main.main_screen_base import MainScreenBase
from controllers.main.main_screen_manager import MainScreenManager
from controllers.partials.numpad import NumPad
from library.utils import Utils

logger = logging.getLogger(__name__)


class HomeScreen(MainScreenBase):
    # btcprice and btcprice_time are updated by MainApp.update_btcdata().
    btcprice = NumericProperty(0)  # type: int  # In cents
    btcprice_time = StringProperty()  # HH:MM

    payment_amount = NumericProperty(0)  # type: int  # In cents
    payment_satoshi = NumericProperty(0)  # type: int  # In satoshis

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.btcprice = self.app.btcprice
        self.btcprice_time = self.app.btcprice_time

        if self.manager.get_interscreen_data('clear_inputted_data'):
            self.clear_inputted_data()

    def on_enter(self, *args):
        super().on_enter(*args)

        # Check if LND is available.
        # TODO: The following codes do not work with invoice.macaroon. Need some workaround...
        # try:
        #     if self.app.lnd:
        #         self.app.lnd.getinfo()
        #     else:
        #         self.message = self.app.messenger.warning('lnd_unavailable')
        # except LndException as e:
        #     self.app.lnd = None
        #     if e.reason == LndException.NOT_CONNECTED:
        #         self.message = self.app.messenger.warning('lnd_not_connected')
        #     elif e.reason == LndException.NOT_UNLOCKED:
        #         self.message = self.app.messenger.warning('lnd_not_unlocked')

    def on_leave(self, *args):
        super().on_leave(*args)

        self.ids.numpad.number_display = ''

        if self.manager.current != 'wait_fiat' and self.manager.current != 'wait_lnd':
            self.clear_inputted_data()

    def clear_inputted_data(self):
        self.ids.numpad.number_display = ''
        self.ids.item_list.clear_items()

    def on_btcprice(self, instance, btcprice):
        self._update_payment_satoshi(btcprice, self.payment_amount)

    def on_payment_amount(self, instance, payment_amount):
        self._update_payment_satoshi(self.app.btcprice, payment_amount)

    def _update_payment_satoshi(self, btcprice: int, payment_amount: int):
        if payment_amount == 0 or btcprice == 0:
            self.payment_satoshi = 0
        else:
            self.payment_satoshi = Utils.fiat_to_satoshi(payment_amount, btcprice)

    def popup_payment_method(self):
        if self.payment_amount == 0:
            self.message = self.app.messenger.warning('payment_amount_zero')
            return

        PaymentMethodPopup().open(self.payment_amount)


class ItemList(RecycleView):
    items = ListProperty()
    """
    Items to be paid.
    Note: 'index' is automatically set by on_items().
    (e.g.)
    self.items.insert(0, {
        'index': None,
        'note': None,
        'price': 300,
    })
    """

    def __init__(self, **kwargs):
        """Note: At this moment, the screen is not initialized."""
        super().__init__(**kwargs)
        self.screen = ...  # type: HomeScreen
        Clock.schedule_once(self.on_init)

    def on_init(self, dt):
        app = App.get_running_app()
        self.screen = app.screen_manager.current_screen

    def on_items(self, instance, items):
        """
        Sets self.items index, and calculates amount.
        Called automatically when self.items been changed.
        """
        payment_amount = 0
        for key, item in enumerate(items):
            item['index'] = key
            payment_amount += item['price']
        self.screen.payment_amount = payment_amount

    def delete_item(self, index: int):
        """
        Deletes an item.
        :param index:
        """
        del self.items[index]

    def clear_items(self):
        """
        Deletes all items.
        """
        # Note 1: I don't know why, but `self.items.clear()` doesn't work.
        # Note 2: Sometimes this causes odd errors. [issues 5986](https://github.com/kivy/kivy/issues/5986)
        self.items = []


class Item(BoxLayout):
    index = NumericProperty(allownone=True)
    note = StringProperty(allownone=True)
    price = NumericProperty(0)  # type: int  # In cents


class NumPadInput(NumPad):

    def push_image_button(self):
        """
        Adds an item to the item list
        """
        number_display = self.number_display.rstrip('.')

        if not number_display:
            self.screen.message = self.app.messenger.warning('payment_not_entered')
            return

        item_price = self.app.fiat.dollar_to_cent(Decimal(number_display))  # type: int  # In cents

        self.screen.ids.item_list.items.insert(0, {
            'index': None,  # TODO
            'note': None,  # TODO
            'price': item_price,
        })

        self.number_display = ''


class PaymentMethodPopup(Popup):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()  # type: MainApp
        self.screen_manager = self.app.screen_manager  # type: MainScreenManager

    def open(self, payment_amount: int, *args, **kwargs):
        super().open(*args, **kwargs)

        grid_layout = self.ids.grid  # type: GridLayout
        grid_layout.cols = 3

        grid_layout.add_widget(Button(
            text=self.app.m('fiat_button'),
            on_release=lambda x: self.push_fiat_payment_button(payment_amount),
        ))

        if self.app.lnd:
            grid_layout.add_widget(Button(
                text=self.app.m('lightning_payment_button'),
                on_release=lambda x: self.push_lightning_payment_button(payment_amount),
            ))
        else:
            grid_layout.add_widget(Widget())

    def on_open(self):
        super().on_open()
        self.app.enable_update_btcdata = False

    def on_dismiss(self):
        super().on_dismiss()
        self.app.enable_update_btcdata = True

    def push_fiat_payment_button(self, payment_amount: int):
        """
        Fiat
        :param payment_amount:
        """
        # Sends payment data to the sub process
        self.app.send_data_to_subproc('screen', 'fiat')
        self.app.send_data_to_subproc('payment_fiat', payment_amount)

        self.dismiss()

        # Go to next screen
        self.screen_manager.transition.direction = 'left'
        self.screen_manager.set_interscreen_data('payment_fiat', payment_amount)
        self.screen_manager.load_screen('wait_fiat')

    def push_lightning_payment_button(self, payment_amount: int):
        """
        BTC Lightning Network
        :param payment_amount:
        """
        from api.lnd import Lnd
        lnd = self.app.lnd  # type: Lnd
        screen = self.screen_manager.current_screen  # type: HomeScreen
        shop_name = self.app.app_config.get('app', 'shop_name')

        btcprice = self.app.btcprice
        btcprice_time = self.app.btcprice_time
        payment_satoshi = Utils.fiat_to_satoshi(payment_amount, btcprice)

        # Make a lnd invoice
        if not lnd:
            screen.message = self.app.messenger.error('lnd_invalid_conf')
            self.dismiss()
            return
        try:
            r_hash, add_index, payment_request = lnd.add_invoice(
                value=payment_satoshi,
                memo='[{}] {} {:,}'.format(shop_name, self.app.fiat.symbol, self.app.fiat.cent_to_dollar(payment_amount)),
                expiry=3 * 60,
            )
        except LndException as e:
            logger.warning(e.args)
            screen.message = self.app.messenger.error('lnd_unable_create_invo')
            self.dismiss()
            return

        # Sends payment data to the sub process
        self.app.send_data_to_subproc('screen', 'qr')
        self.app.send_data_to_subproc(
            'payment',
            (btcprice, btcprice_time, payment_satoshi, payment_amount, payment_request)
        )

        self.dismiss()

        # Go to next screen
        self.screen_manager.transition.direction = 'left'
        self.screen_manager.set_interscreen_data(
            'invoice',
            (r_hash, add_index, payment_request, btcprice, btcprice_time, payment_satoshi, payment_amount)
        )
        self.screen_manager.load_screen('wait_lnd')

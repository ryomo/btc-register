from kivy.app import App
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from controllers.main.main_app import MainApp


class NumPad(BoxLayout):
    MAX_DIGITS = 12

    number_display = StringProperty()  # type: str

    def __init__(self, **kwargs):
        """Note: At this moment, the screen is not initialized."""
        super().__init__(**kwargs)
        self.app = App.get_running_app()  # type: MainApp
        self.screen = ...  # type: Screen

        Clock.schedule_once(self.on_init)

    def on_init(self, dt):
        self.screen = self.app.screen_manager.current_screen

        if self.app.fiat.has_dot():
            self.ids.num_button_optional.text = '.'
            self.ids.num_button_optional.on_release = self.push_dot_button
        else:
            self.ids.num_button_optional.text = '00'
            self.ids.num_button_optional.on_release = lambda: self.push_num_button('00')

    def push_num_button(self, button_text: str):
        if button_text == '0':
            if self.app.fiat.has_dot() and self.number_display == '0':
                return
            elif not self.app.fiat.has_dot() and self.number_display == '':
                return

        # Checks total digits. This cointains decimal point.
        if len(self.number_display) >= self.MAX_DIGITS:
            return

        # Checks digits after decimal point.
        splitted_numbers = self.number_display.split('.')
        if len(splitted_numbers) == 2 and len(splitted_numbers[1]) >= self.app.fiat.max_digits_after_point():
            return

        self.number_display += button_text

    def push_dot_button(self):
        if '.' in self.number_display:
            return

        if self.number_display == '':
            self.number_display = '0'

        self.number_display += '.'

    def push_delete_button(self):
        if self.number_display != '':
            self.number_display = self.number_display[:-1]

    def push_image_button(self):
        pass

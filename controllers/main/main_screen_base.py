import logging

from kivy.app import App
from kivy.properties import StringProperty

from controllers.main.main_app import MainApp
from controllers.screen_base import ScreenBase

logger = logging.getLogger(__name__)


class MainScreenBase(ScreenBase):
    message = StringProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()  # type: MainApp

    def on_touch_down(self, touch):
        self.message = ''
        return super().on_touch_down(touch)

import logging

from kivy.app import App
from kivy.clock import Clock

from controllers.screen_manager_base import ScreenManagerBase

logger = logging.getLogger(__name__)


class SubScreenManager(ScreenManagerBase):

    def __init__(self, pipe, **kwargs):
        super().__init__(**kwargs)
        self._app = App.get_running_app()
        Clock.schedule_interval(self.update, 1 / 30)

    def update(self, dt):
        screen_name = self._app.receive_data_from_mainproc('screen')
        if screen_name:
            self.load_screen(screen_name)

    def load_screen(self, screen_name, process='sub'):
        super().load_screen(screen_name, process)

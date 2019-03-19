import logging

from kivy.app import App

from controllers.screen_base import ScreenBase
from controllers.sub.sub_app import SubApp

logger = logging.getLogger(__name__)


class SubScreenBase(ScreenBase):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()  # type: SubApp

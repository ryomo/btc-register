import logging
from importlib import import_module

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from library.utils import Utils
from run import APP_PATH

logger = logging.getLogger(__name__)


class ScreenManagerBase(ScreenManager):

    def load_screen(self, screen_name, process):
        """
        Imports the screen if not exists, and changes current screen to it.
        :param screen_name:
        :param process:
        """
        if not self.has_screen(screen_name):
            Builder.load_file(APP_PATH + '/views/{}/{}_screen.kv'.format(process, screen_name))

            screen_module = import_module('controllers.{}.{}_screen'.format(process, screen_name))
            screen_class_name = Utils.snake_to_camel(screen_name) + 'Screen'
            screen = getattr(screen_module, screen_class_name)(name=screen_name)
            self.add_widget(screen)

        self.current = screen_name

        self.current = screen_name
        logger.info('SCREEN: [{}] {}'.format(process.upper(), self.current))

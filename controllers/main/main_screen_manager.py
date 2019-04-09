import logging

from controllers.screen_manager_base import ScreenManagerBase

logger = logging.getLogger(__name__)


class MainScreenManager(ScreenManagerBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._interscreen_data = None
        """Data to be used across each screens."""

    def load_screen(self, screen_name, process='main'):
        super().load_screen(screen_name, process)

    def set_interscreen_data(self, key: str, value):
        """
        Sets data to be used across each screens.
        (e.g.)
        self.manager.set_interscreen_data('data_name', ('some', 'test', 'data'))
        self.load_screen('screen_name')
        ...
        some, test, data = self.manager.get_interscreen_data('data_name')
        :param key:
        :param value:
        """
        logger.debug('INTERSCREEN: set: {}'.format((key, value)))
        self._interscreen_data = (key, value)

    def get_interscreen_data(self, key: str):
        """
        Gets data set by set_interscreen_data, and delete it.
        (e.g.)
        some, test, data = self.manager.set_interscreen_data('data_name')
        :return:
        """
        if self._interscreen_data and self._interscreen_data[0] == key:
            tmp_interscreen_data = self._interscreen_data[1]
            logger.debug('INTERSCREEN: get: {}'.format(self._interscreen_data))
            self._interscreen_data = None
            return tmp_interscreen_data
        else:
            return None

import logging

from kivy.core.window import Window
from kivy.uix.vkeyboard import VKeyboard

from controllers.main.main_screen_base import MainScreenBase

logger = logging.getLogger(__name__)


class LndUnlockScreen(MainScreenBase):
    # TODO: Not works for now, because of kivy's keyboard problems.
    #  * kivyのconfig.iniでkeyboard_mode='dock'とすると、他のTextInputでもVKeyboardが有効になってしまう。
    #  * real keyboardには2重入力の問題がある。
    #  * ここではなぜかTextInputのfocus=Trueが動かない。 [#3863](https://github.com/kivy/kivy/issues/3863)

    def __init__(self, **kw):
        super().__init__(**kw)

        kb = Window.request_keyboard(self._keyboard_close, self.ids.text_input)
        self._keyboard = kb.widget  # type: VKeyboard
        # logger.debug('TEST: {}'.format(self._keyboard.size))
        # self._keyboard.size = [800, 300]

    def on_enter(self, *args):
        super().on_enter(*args)
        # self._keyboard.target = self.ids.text_input
        # self.ids.text_input.target = True

    def _keyboard_close(self, *args):
        if self._keyboard:
            # self._keyboard.unbind(on_key_down=self.key_down)
            # self._keyboard.unbind(on_key_up=self.key_up)
            self._keyboard = None

    # def key_up(self, keyboard, keycode, *args):
    #     """ The callback function that catches keyboard events. """
    #     pass

import logging
from importlib import import_module

from messages.messages_en import messages as default_messages

logger = logging.getLogger(__name__)


class Messenger:
    DEFAULT_LANG = 'en'

    def __init__(self, lang='en'):
        if lang == self.DEFAULT_LANG:
            self.messages = default_messages
        else:
            # Import `messages` module dynamically.
            messages_module = import_module('messages.messages_{}'.format(lang))
            messages = getattr(messages_module, 'messages')

            # Merge dicts
            self.messages = {
                **default_messages,
                **messages,
            }

    def get_text(self, key: str) -> str:
        return self.messages[key]

    def info(self, key):
        return self.get_text(key)

    def warning(self, key):
        return '[color=ffff33]WARNING:[/color] {}'.format(self.get_text(key))

    def error(self, key):
        return '[b][color=ff3333]ERROR:[/color] {}[/b]'.format(self.get_text(key))

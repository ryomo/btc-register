import logging
from typing import Callable

from kivy.clock import ClockEvent, Clock
from kivy.uix.screenmanager import Screen

logger = logging.getLogger(__name__)


class ScreenBase(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.clock_events = []  # type: [ClockEvent]

    def on_leave(self, *args):
        for clock_event in self.clock_events:
            clock_event.cancel()

    def schedule_interval(self, callback: Callable, delay=0):
        """
        :param callback: e.g. `def callback(self, dt)`
        :param delay: The interval in seconds.
        """
        self.clock_events.append(Clock.schedule_interval(callback, delay))

    def schedule_once(self, callback: Callable, delay=0):
        """
        :param callback: e.g. `def callback(self, dt)`
        :param delay: The delay before the call in seconds.
        """
        self.clock_events.append(Clock.schedule_once(callback, delay))

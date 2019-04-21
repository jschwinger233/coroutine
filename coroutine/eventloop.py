import asyncio
import selectors
from numbers import Real
from collections import deque
from selectors import EVENT_WRITE, EVENT_READ

from tracemalloc import Frame
from typing import IO, Callable, Optional

from .utils import singleton
from .fd_pool import FDPool

SelectorEvent = type(selectors.EVENT_READ)


@singleton
class EventLoop(asyncio.AbstractEventLoop):

    @classmethod
    def get_event_loop(cls):
        return cls.get_instance()

    def __init__(self):
        self._running = False
        self._ready = deque()
        self._selector = selectors.DefaultSelector()
        self._fd_pool = FDPool.get_instance()

    def run_forever(self):
        self._running = True
        while self._running:
            while self._ready:
                callback = self._ready.pop()
                callback()

            for key, event in self._selector.select():
                callback = key.data['callback']
                callback(key.fileobj, event, self)

    def add_reader(
        self, fd: IO,
        callback: Callable[[IO, SelectorEvent, 'EventLoop'], None]
    ):
        data = {'callback': callback}
        self._selector.register(fd, EVENT_READ, data)

    def add_writer(
        self, fd: IO,
        callback: Callable[[IO, SelectorEvent, 'EventLoop'], None]
    ):
        data = {'callback': callback}
        self._selector.register(fd, EVENT_WRITE, data)

    def remove_reader(self, fd: IO) -> bool:
        try:
            self._selector.get_key(fd)
        except KeyError:
            return False
        else:
            self._selector.unregister(fd)
            return True

    remove_writer = remove_reader

    def call_soon(self, callback: Callable[[], None]):
        self._ready.appendleft(callback)

    def call_later(
        self,
        delay: Real,
        func: Callable[[], None],
    ):

        def callback(fd: IO, event: SelectorEvent, event_loop: EventLoop):
            fd.read()
            event_loop.remove_reader(fd)
            func()

        fd = self._fd_pool.get_timerfd(delay)
        self.add_reader(fd, callback)

    def add_signal_handler(
        self,
        sig: int,
        func: Callable[[int, Optional[Frame]], None],
    ):

        def callback(fd: IO, event: SelectorEvent, event_loop: EventLoop):
            status = fd.read()
            func(status['signo'], None)

        fd = self._fd_pool.get_signalfd(sig)
        self.add_reader(fd, callback)

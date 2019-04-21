from functools import wraps, partial
from greenlet import greenlet as Greenlet
from typing import Optional, Callable, Sequence, Mapping

from .fd_pool import FDPool
from .eventloop import EventLoop

EVENT_LOOP_COROUTINE = None


class Coroutine:
    _fd_pool = FDPool.get_instance()

    @classmethod
    def current(cls):
        return cls(greenlet=Greenlet.getcurrent())

    def __init__(
        self,
        target: Optional[Callable] = None,
        args: Optional[Sequence] = None,
        kwargs: Optional[Mapping] = None,
        *,
        greenlet: Optional[Greenlet] = None,
    ):
        args = args or ()
        kwargs = kwargs or {}

        if greenlet:
            target = greenlet.switch

        @wraps(target)
        def wrapper():
            target(*args, **kwargs)
            self._alive = False
            if self._finish_fd:
                self._finish_fd.write()

        self.greenlet = Greenlet(wrapper)
        if target != EventLoop.get_instance().run_forever:
            self.greenlet.parent = get_event_loop_coroutine().greenlet

        self._alive = False
        self._finish_fd = None

    def _resume(self):
        return self.greenlet.switch()

    def start(self, *, sched_first=True):
        self._alive = True
        event_loop = EventLoop.get_instance()
        event_loop.call_soon(self.greenlet.switch)
        if sched_first:
            event_loop.call_soon(resume_current())
            yield_current()

    def is_alive(self) -> bool:
        return self._alive

    def join(self):
        if not self.is_alive():
            return

        def callback(resume, _, __, event_loop):
            event_loop.remove_reader(self._finish_fd)
            resume()

        event_loop = EventLoop.get_instance()
        self._finish_fd = self._fd_pool.get_eventfd()
        event_loop.add_reader(
            self._finish_fd, partial(callback, resume_current())
        )
        yield_current()


def resume_current():
    coro = Coroutine.current()
    return coro._resume


def yield_current():
    event_loop_coro = get_event_loop_coroutine()
    event_loop_coro._resume()


def get_event_loop_coroutine():
    global EVENT_LOOP_COROUTINE
    if not EVENT_LOOP_COROUTINE:
        event_loop = EventLoop.get_instance()
        EVENT_LOOP_COROUTINE = Coroutine(event_loop.run_forever)
    return EVENT_LOOP_COROUTINE

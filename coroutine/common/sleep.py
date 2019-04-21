from numbers import Real
from ..eventloop import EventLoop
from ..coroutine import resume_current, yield_current


def sleep(sec: Real):
    event_loop = EventLoop.get_instance()

    if sec == 0:
        event_loop.call_soon(resume_current())
    else:
        event_loop.call_later(sec, resume_current())

    yield_current()

from tracemalloc import Frame
from typing import Callable, Optional

from ..eventloop import EventLoop
from ..coroutine import Coroutine


def signal(
    signum: int,
    handler: Callable[[int, Optional[Frame]], None],
):

    def callback(sig: int, frame: Optional[Frame]):
        Coroutine(target=handler, args=(sig, frame)).start()

    event_loop = EventLoop.get_instance()
    event_loop.add_signal_handler(signum, callback)

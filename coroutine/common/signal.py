from tracemalloc import Frame
from typing import Callable, Optional

from ..eventloop import EventLoop


def signal(
    signum: int,
    handler: Callable[[int, Optional[Frame]], None],
):
    event_loop = EventLoop.get_instance()
    event_loop.add_signal_handler(signum, handler)

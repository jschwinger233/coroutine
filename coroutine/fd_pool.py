import linuxfd
from numbers import Real
from typing import IO
from pysigset import (
    sigprocmask, sigaddset, SIG_BLOCK, SIG_UNBLOCK, SIGSET, NULL
)

from .utils import singleton


@singleton
class FDPool:

    def __init__(self):
        self._close_on_fork = set()

    def get_timerfd(
        self,
        delay: Real,
        interval: Real = 0,
        *,
        close_on_fork=True,
    ) -> IO:
        fd = linuxfd.timerfd(rtc=True, nonBlocking=True)
        if close_on_fork:
            self._close_on_fork.add(fd)

        fd.settime(delay, interval)
        return fd

    def get_signalfd(self, sig: int, *, close_on_fork=True) -> IO:
        sigset = SIGSET()
        sigaddset(sigset, sig)
        sigprocmask(SIG_BLOCK, sigset, NULL)

        fd = linuxfd.signalfd(signalset={sig}, nonBlocking=True)
        if close_on_fork:
            self._close_on_fork.add(fd)

        return fd

    def get_eventfd(self, *, close_on_fork=True) -> IO:
        fd = linuxfd.eventfd(initval=0, nonBlocking=True)
        if close_on_fork:
            self._close_on_fork.add(fd)

        return fd

    def release(self, fd: IO):
        # TODO: singledispatch
        if fd not in self._close_on_fork:
            return

        self._close_on_fork.remove(fd)
        fd.close()

        if isinstance(fd, linuxfd.signalfd):
            sigset = SIGSET()
            for sig in fd.signals():
                sigaddset(sigset, sig)
            sigprocmask(SIG_UNBLOCK, sigset, NULL)

    def on_fork(self):
        while self._close_on_fork:
            fd = next(iter(self._close_on_fork))
            self.release(fd)

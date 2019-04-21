import socket as _socket
from functools import partial

from ..eventloop import EventLoop
from ..coroutine import resume_current, yield_current


class SocketFactory:

    def create(self, family, type):
        if family != _socket.AF_UNIX and type != _socket.SOCK_DGRAM:
            raise NotImplementedError

        return UnixUdpSocket()


class UnixUdpSocket:

    def __init__(self):
        self.sock = _socket.socket(_socket.AF_UNIX, _socket.SOCK_DGRAM)
        self.sock.setblocking(0)

    def __getattr__(self, attr):
        return getattr(self.sock, attr)

    def recvfrom(self, buffersize: int):
        try:
            return self.sock.recvfrom(buffersize)
        except BlockingIOError:

            def callback(resume, _, __, event_loop):
                event_loop.remove_reader(self.sock)
                resume()

            event_loop = EventLoop.get_event_loop()
            event_loop.add_reader(
                self.sock, partial(callback, resume_current())
            )
            yield_current()
            return self.sock.recvfrom(buffersize)


def socket(family=_socket.AF_INET, type=_socket.SOCK_STREAM):
    sock_factory = SocketFactory()
    return sock_factory.create(family, type)

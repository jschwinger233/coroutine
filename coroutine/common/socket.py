import socket as _socket
from functools import partial

from ..fd_pool import FDPool
from ..eventloop import EventLoop
from ..coroutine import resume_current, yield_current


class SocketFactory:
    fd_pool = FDPool.get_instance()

    def create(self, family, type):
        if family != _socket.AF_UNIX and type != _socket.SOCK_DGRAM:
            raise NotImplementedError

        sock = self.fd_pool.get_socket(family, type)
        return UnixUdpSocket(sock)


class UnixUdpSocket:

    def __init__(self, sock):
        self.sock = sock

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

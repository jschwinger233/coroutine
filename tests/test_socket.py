import os
import socket
import coroutine
from contextlib import suppress

addr = '/tmp/b.sock'
with suppress(FileNotFoundError):
    os.remove(addr)
sock = coroutine.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
sock.bind(addr)


def serve_forever():
    while True:
        msg, addr = sock.recvfrom(1024)
        print(f'receive {msg} from {addr}')


def heartbeat():
    while True:
        print('beating')
        coroutine.sleep(1)


if __name__ == '__main__':
    coroutine.Coroutine(target=heartbeat).start()
    server = coroutine.Coroutine(target=serve_forever)
    server.start()
    server.join()

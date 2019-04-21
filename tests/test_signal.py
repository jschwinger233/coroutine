import signal
import coroutine


def handler(sig, frame):
    print(12)
    coroutine.sleep(4)
    print(34)
    global exit
    exit = True


if __name__ == '__main__':
    exit = False
    coroutine.signal(signal.SIGINT, handler)
    while not exit:
        coroutine.sleep(0.2)
        print('waiting')

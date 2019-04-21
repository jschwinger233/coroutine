import coroutine


def f(x):
    print(12)
    coroutine.sleep(x)
    print(34)


if __name__ == '__main__':
    coro = coroutine.Coroutine(target=f, args=(2,))
    coro.start()
    print(56)
    coro.join()

# coroutine

[coroutine](https://github.com/jschwinger23/coroutine) is a package that supports spawning coroutine using an API similar to the [threading](https://docs.python.org/3/library/threading.html#module-threading) module.

## Introduction

```python
import coroutine

def f(x):
    print(12)
    coroutine.sleep(x)
    print(34)

if __name__ == '__main__':
    coro = coroutine.Coroutine(target=f, args=(1,))
    coro.start()
    print(56)
    coro.join()
```

output is obvious:

```
12
56
34
```

## Coroutine Objects

### `coroutine.Coroutine(target=None, args=(), kwargs={})`

#### `start()`

start the coroutine's activity.

#### `run()`

Method representing the coroutine's activity.

#### `join(timeout=None)`

Wait until the coroutine terminates. This blocks the calling coroutine until the coroutine whose `join()` method is called terminated, or until the optional timeout occurs.

#### `is_alive()`

Return whether the coroutine is alive.

#### `ident`

The coroutine identifier of this coroutine.

## Common Functions

### Sleep

**coroutine.sleep(seconds=0)**

Put he current coroutine to sleep for at least seconds.

This has to be used in coroutine instead of `time.sleep`.

### Signal

**coroutine.signal(signalnum, handler)**

Call the handler when the process receives the signal *signalnum*.

This has to be used in coroutine instead of `signal.signal`.

### Pipe

**coroutine.pipe(flags)**

Create a pipe with *flags* set. Flags can be `O_CLOEXEC`. Return a pair of file descriptors `(r, w)` usable for reading and writing.

This has to be used in coroutine instead of `os.pipe` or `os.pipe2`.

### Socket

**coroutine.socket(family=AF_INET, type=SOCK_STREAM)**

Create a new socket using the given address family and socket type.

**ATTENTION:** at present only `AF_UNIX` is supported, 233333.

This has to be used in coroutine instead of `socket.socket`.

## Rationale

In Python world there are a few options to write asynchronous code:

* `async`
* `Twisted`
* `Gevent`
* `Tornado`

However none of those is silver bullet.

`async`, piece of shit; `Twisted`, too old-style; `Gevent`, magic but implicit; `Tornado`, ugly syntax and performance issue.

Under most of situations, Gevent is my best choice, but I believe some more explicit API can be of value, especially when no socket is involved like process management.

In the mean time, the complex implementation of Gevent eludes me always: why there isn't a API conforming to [PEP-3156](https://www.python.org/dev/peps/pep-3156/); what the fuck is [`hub`](http://www.gevent.org/_modules/gevent/hub.html); why self-pipe trick isn't made good use; why [`timer_fd`](http://man7.org/linux/man-pages/man2/timerfd_create.2.html) is ignored.

Then I give you this module.

## Implementation

omit

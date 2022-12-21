import time
from contextlib import contextmanager


@contextmanager
def timing(message=None):
    start = time.time()
    yield start
    end = time.time()
    if message:
        print(message, end - start, "seconds")
    else:
        print(end - start, "seconds")


def cumsum(array):
    result = list()
    x = 0
    for a in array:
        x = x + a
        result.append(x)
    return result

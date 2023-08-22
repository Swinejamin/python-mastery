import os
import time

# Decorator for coroutine functions
from functools import wraps


# Data source
def follow(filename, target):
    with open(filename, "r") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if line != "":
                target.send(line)
            else:
                time.sleep(0.1)


def consumer(func):
    @wraps(func)
    def start(*args, **kwargs):
        f = func(*args, **kwargs)
        f.send(None)
        return f

    return start


@consumer
def printer():
    while True:
        try:
            item = yield
            print(item)
        except Exception as e:
            print("ERROR: %r" % e)


# Example use
if __name__ == "__main__":
    p = printer()
    p.send("hello")

    p.send(42)

    p.throw(ValueError("It failed"))
    try:
        int("n/a")
    except ValueError as e:
        p.throw(e)

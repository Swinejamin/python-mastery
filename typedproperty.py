from collections.abc import Callable
from pprint import pprint
from typing import Any
from functools import wraps
from inspect import getsource, get_annotations


def my_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        print(getsource(f))
        print(get_annotations(f))

        print(f"Calling decorated function {f.__str__()}")
        for arg in args:
            print(arg)

        for arg in kwds:
            print(arg)

        return f(*args, **kwds)

    return wrapper


def typedproperty(
    expected_type,
):
    private_name = f"_{__name__}"

    @property
    def value(self) -> expected_type:
        # pprint(self)

        return getattr(self, private_name)

    @value.setter
    def value(self, val):
        if not isinstance(val, expected_type):
            raise TypeError(f"Expected {expected_type}")

        pprint(self)
        # self.public_name = name
        # self.private_name = "_" + name

        setattr(self, private_name, val)

    return value


String = my_decorator(lambda: typedproperty(expected_type=str))


# @my_decorator
# def String():
#     pprint(locals())
#     return typedproperty(expected_type=str)


Integer: Callable[[Any], property] = my_decorator(lambda: typedproperty(int))
Float: Callable[[Any], property] = my_decorator(lambda: typedproperty(float))


if __name__ == "__main__":

    class Stock:
        name = String()
        shares = Integer()
        price = Float()

        def __init__(self, name, shares, price):
            self.name = name
            self.shares = shares
            self.price = price

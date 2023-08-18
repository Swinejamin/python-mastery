from structure import Structure
import inspect
from collections import namedtuple

from validate import ValidatedFunction, Integer


class Stock(Structure):
    _fields = ('name', 'shares', 'price')

    @property
    def cost(self):
        return self.shares * self.price

    @ValidatedFunction
    def sell(self, nshares: Integer):
        self.shares -= nshares


Stock.create_init()

s = Stock('GOOG', 100, 490.1)
s.sell(10)

from structure import Structure

import reader


class Stock(Structure):
    name = String()
    shares = PositiveInteger()
    price = PositiveFloat()

    @property
    def cost(self):
        return self.shares * self.price

    def sell(self, nshares):
        self.shares -= nshares


s = Stock("GOOG", 100, 490.1)
s2 = Stock("GOOG", 100, 490.1)


print(s == s2)
print(list(s))
print(tuple(s))

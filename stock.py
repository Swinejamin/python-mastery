from pprint import pprint
from sys import intern
from decimal import Decimal

import reader
import tableformat


class Stock:
    types = (str, int, float)

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    @classmethod
    def from_row(cls, row):
        try:
            values = [func(val) for func, val in zip(cls.types, row.values())]

            return cls(*values)

        except Exception as e:
            print(e)

    def cost(self):
        return self.shares * self.price

    def sell(self, nshares):
        self.shares -= nshares


class DStock(Stock):
    types = (str, int, Decimal)


def read_portfolio(filename="Data/portfolio.csv", cls=Stock):

    rows = reader.read_file_as_type(
        filename=filename,
        type_name="data_collection",
        converters=[intern, int, float],
    )

    stocks = list()

    for row in rows:
        result = cls.from_row(row)
        stocks.append(result)

    # final = [Stock(name, shares, price) for (name, shares, price) in rows]

    return stocks


def print_portfolio(p):
    tableformat.print_table(p, ["name", "shares", "price"])
    # print("%10s %10s %10s" % ("name", "shares", "price"))
    # print(("-" * 10 + " ") * 3)
    # for s in p:
    #     print("%10s %10d %10.2f" % (s.name, s.shares, s.price))


portfolio = read_portfolio()
Dportfolio = read_portfolio(cls=DStock)

print_portfolio(portfolio)

print()
print()
print()
print()
print()

print_portfolio(Dportfolio)

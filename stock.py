from pprint import pprint
import sys
from sys import intern, stdout
from decimal import Decimal
from colored import Fore, Back, Style

from validate import PositiveFloat, PositiveInteger, Positive, String, NonEmptyString

import reader
from tableformat import (
    create_formatter,
    print_table,
    TextTableFormatter,
    UpperHeadersMixin,
)


class redirect_stdout:
    def __init__(self, out_file):
        self.out_file = out_file

    def __enter__(self):
        self.stdout = sys.stdout
        sys.stdout = self.out_file
        return self.out_file

    def __exit__(self, ty, val, tb):
        sys.stdout = self.stdout


class Stock:
    _types = {"name": str, "shares": int, "price": float}

    name = NonEmptyString()
    shares = PositiveInteger()
    price = PositiveFloat()

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    def __repr__(self):
        return f"Stock({self.name!r}, {self.shares!r}, {self.price!r})"

    @classmethod
    def from_row(cls, row):
        values = [func(val) for func, val in zip(cls._types.values(), row)]
        return cls(*values)

    @property
    def cost(self):
        return self.shares * self.price

    def sell(self, nshares):
        self.shares -= nshares


class DStock(Stock):
    __slots__ = ("name", "_shares", "_price")
    _types = {"name": str, "shares": int, "price": Decimal}

    @Stock.cost.getter
    def cost(self):
        return Decimal(self._shares) * self._price


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


portfolio = reader.read_csv_as_instances(filename="Data/portfolio.csv", cls=Stock)

format_list = [
    {"name": "text", "column_formats": ['"%s"', "%d", "%0.2f"]},
    {"name": "text", "upper_headers": True},
    {"name": "csv", "upper_headers": False},
    {"name": "csv", "upper_headers": True, "column_formats": ['"%s"', "%d", "%0.2f"]},
    {"name": "html", "upper_headers": False},
    {"name": "html", "upper_headers": True, "column_formats": ['"%s"', "%d", "%0.2f"]},
]


def check_formatters():
    for format_to_use in format_list:
        formatter = create_formatter(**format_to_use)
        print_table(portfolio, ["name", "shares", "price"], formatter)


check_formatters()

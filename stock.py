from pprint import pprint
import sys
from sys import intern, stdout
from decimal import Decimal
from colored import Fore, Back, Style

from validate import PositiveFloat, PositiveInteger, Positive

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
    __slots__ = ("name", "_shares", "_price")
    _types = {"name": str, "shares": int, "price": float}

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    def __repr__(self):
        # Note: The !r format code produces the repr() string
        return f"{type(self).__name__}({f'{Fore.blue + Style.bold}{self.name!r}{Style.reset}'}, {Fore.cyan}{self.shares!r}{Style.reset}, {Fore.green}{self.price!r}{Style.reset})"

    def __eq__(self, other):
        return isinstance(other, Stock) and (
            (self.name, self.shares, self.price)
            == (other.name, other.shares, other.price)
        )

    @classmethod
    def from_row(cls, row):
        values = [func(val) for func, val in zip(cls._types.values(), row)]
        return cls(*values)

    @classmethod
    def check_type(cls, value, type_key):
        type_to_check = cls._types.get(type_key)
        if not isinstance(value, type_to_check):
            try:
                converted_value = type_to_check(value)

                print(
                    f"Value for {type_key} ({value}) converted from {type(value).__name__} to {type_to_check.__name__} ({converted_value})"
                )

                return converted_value

            except ValueError:
                raise TypeError(
                    f"Expected {type_to_check.__name__}, received --{value}-- with type {type(value).__name__}"
                )

        return value

    @property
    def shares(self):
        return self._shares

    @shares.setter
    def shares(self, value):
        self._shares = PositiveInteger.check(value)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = PositiveFloat.check(value)

    @property
    def cost(self):
        return self._shares * self._price

    def sell(self, nshares):
        self._shares -= Positive.check(nshares)


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

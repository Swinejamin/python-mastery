from pprint import pprint
from sys import intern
from decimal import Decimal

import reader
from tableformat import create_formatter, print_table


class Stock:
    __slots__ = ("name", "_shares", "_price")
    _types = {"name": str, "shares": int, "price": float}

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

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
        converted_value = self.check_type(value, "shares")

        if converted_value < 0:
            raise ValueError("shares must be >= 0")
        self._shares = converted_value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        converted_value = self.check_type(value, "price")
        if converted_value <= 0:
            raise ValueError("price must be > 0")
        self._price = converted_value

    @property
    def cost(self):
        return self._shares * self._price

    def sell(self, nshares):
        self._shares -= nshares

    def __repr__(self):
        return


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


# portfolio = reader.read_csv_as_instances("Data/portfolio.csv", Stock)
# formatter = create_formatter("text")
# print_table(portfolio, ["name", "shares", "price"], formatter)
# formatter = create_formatter("csv")
# print_table(portfolio, ["name", "shares", "price"], formatter)
# formatter = create_formatter("html")
# print_table(portfolio, ["name", "shares", "price"], formatter)

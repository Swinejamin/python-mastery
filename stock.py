from pprint import pprint
from sys import intern

import reader


class Stock:
    def __init__(self, name, shares, price):

        self.name = name
        self.shares = shares
        self.price = price

    def cost(self):
        return self.shares * self.price

    def sell(self, nshares):
        self.shares -= nshares


def read_portfolio(filename="Data/portfolio.csv"):

    rows = reader.read_file_as_type(
        filename=filename,
        type_name="data_collection",
        converters=[intern, int, float],
    )

    stocks = list()

    for row in rows:

        stocks.append(Stock(row["name"], row["shares"], row["price"]))

    final = [Stock(name, shares, price) for (name, shares, price) in rows]

    return stocks


def print_portfolio(p):

    print("|  name   |  shares  |   price   |")
    print("---------- ---------- ---------- ")
    for line in p:
        print(f"     {line.name}   |   {line.price}   |   {line.shares}")


s = Stock("GOOG", 100, 490.10)
portfolio = read_portfolio()

print_portfolio(portfolio)

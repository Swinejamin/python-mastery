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


s = Stock.from_row(["GOOG", "100", "490.1"])
print(s)


port = reader.read_csv_as_instances("Data/portfolio.csv", Stock)

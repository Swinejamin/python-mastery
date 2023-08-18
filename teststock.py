import unittest
from stock import Stock


class TestStock(unittest.TestCase):
    def test_create(self):
        s = Stock("GOOG", 100, 490.1)
        self.assertEqual(s.name, "GOOG")
        self.assertEqual(s.shares, 100)
        self.assertEqual(s.price, 490.1)

    def test_create_keyword(self):
        s = Stock(name="GOOG", shares=100, price=490.1)
        self.assertEqual(s.name, "GOOG")
        self.assertEqual(s.shares, 100)
        self.assertEqual(s.price, 490.1)

    # Test that the cost property returns a correct value
    def test_cost_property(self):
        s = Stock("GOOG", 100, 490.1)

        self.assertEqual(s.cost, 49010)

    # Test that the sell() method correctly updates the shares.
    def test_sell(self):
        s = Stock("GOOG", 100, 490.1)

        s.sell(2)
        self.assertEqual(s.shares, 98)
        s.sell(20)
        self.assertEqual(s.shares, 78)

    # Test that the from_row() class method creates a new instance from good data.
    def test_from_row(self):
        row = Stock.from_row(["GOOG", "100", "490.1"])

        self.assertEqual(repr(row), "Stock('GOOG', 100, 490.1)")

    # Test that the __repr__() method creates a proper representation string.
    def test_repr(self):
        s = Stock("GOOG", 100, 490.1)

        self.assertEqual(repr(s), "Stock('GOOG', 100, 490.1)")

    # Test the comparison operator method __eq__()
    def test_eq(self):
        a = Stock("GOOG", 100, 490.1)
        b = Stock("GOOG", 100, 490.1)
        self.assertTrue(a == b)


if __name__ == "__main__":
    unittest.main()

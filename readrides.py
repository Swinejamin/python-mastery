import csv
import tracemalloc
from collections import namedtuple


class Row:
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides


class RowWithSlots:
    # Uncomment to see effect of slots
    __slots__ = ("route", "date", "daytype", "rides")

    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides


# Uncomment to use a namedtuple instead
# from collections import namedtuple
# Row = namedtuple('Row',('route','date','daytype','rides'))


def read_rides_as_dicts(filename):
    """
    Read the bus ride data as a list of dicts
    """
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)  # Skip headers

        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])

            record = {"route": route, "date": date, "daytype": daytype, "rides": rides}
            records.append(record)

    return records


def read_rides_as_instances(filename):
    """
    Read the bus ride data as a list of Class instances
    """
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)  # Skip headers

        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = Row(route, date, daytype, rides)
            records.append(record)

    return records


def read_rides_as_instances_with_slots(filename):
    """
    Read the bus ride data as a list of Class instances
    """
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)  # Skip headers

        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = RowWithSlots(route, date, daytype, rides)
            records.append(record)

    return records


def read_rides_as_tuples(filename):
    """
    Read the bus ride data as a list of tuples
    """
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)  # Skip headers

        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = (route, date, daytype, rides)
            records.append(record)

    return records


RowTuple = namedtuple("Row", ("route", "date", "daytype", "rides"))


def read_rides_as_named_tuples(filename):
    """
    Read the bus ride data as a list of tuples
    """

    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)  # Skip headers

        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = RowTuple(route, date, daytype, rides)

            records.append(record)

    return records


def read_file_as_type(filename, type_name):

    try:
        if type_name == "tuple":
            return read_rides_as_tuples(filename)

        if type_name == "named_tuple":
            return read_rides_as_tuples(filename)

        if type_name == "dict":
            return read_rides_as_dicts(filename)

        if type_name == "instance":
            return read_rides_as_instances(filename)

        if type_name == "slots":
            return read_rides_as_instances_with_slots(filename)

    except Exception as e:
        print(e)

    return read_rides_as_tuples(filename)


if __name__ == "__main__":
    tracemalloc.start()

    # for type_name in ["tuple", "named_tuple", "dict", "instance", "slots"]:
    for function_to_call in [
        read_rides_as_tuples,
        read_rides_as_named_tuples,
        read_rides_as_instances,
        read_rides_as_instances_with_slots,
        read_rides_as_dicts,
    ]:
        tracemalloc.clear_traces()

        # read_file_as_type("Data/ctabus.csv", type_name)
        function_to_call("Data/ctabus.csv")

        current, peak = tracemalloc.get_traced_memory()

        print(
            f"Memory Use for {function_to_call.__name__}: Current {current}, Peak {format(peak,'08,.1f')}"
        )

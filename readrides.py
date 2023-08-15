import csv
import tracemalloc
from collections.abc import Sequence
from collections import namedtuple


class RideData(Sequence):
    def __init__(self):
        self.routes = []  # Columns
        self.dates = []
        self.daytypes = []
        self.numrides = []

    def __len__(self):
        # All lists assumed to have the same length
        return len(self.routes)

    def __getitem__(self, index):
        return {
            "route": self.routes[index],
            "date": self.dates[index],
            "daytype": self.daytypes[index],
            "rides": self.numrides[index],
        }

    def append(self, d):
        self.routes.append(d["route"])
        self.dates.append(d["date"])
        self.daytypes.append(d["daytype"])
        self.numrides.append((d["rides"]))


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
    records = RideData()
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


def read_rides_with_generator(filename):
    f = open(filename)
    f_csv = csv.reader(f)
    headers = next(f_csv)

    # rows = list()
    #
    # for (route, date, daytype, rides) in f_csv:
    #     item = dict(zip(headers, (route, date, daytype, rides)))
    #     if route == "22" and date == "02/02/2011":
    #         pprint(item)
    #
    #     rows.append(item)

    return (dict(zip(headers, row)) for row in f_csv)


def read_rides_as_columns(filename):
    """
    Read the bus ride data into 4 lists, representing columns
    """
    routes = []
    dates = []
    daytypes = []
    numrides = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)  # Skip headers
        for row in rows:
            routes.append(row[0])
            dates.append(row[1])
            daytypes.append(row[2])
            numrides.append(int(row[3]))
    return dict(routes=routes, dates=dates, daytypes=daytypes, numrides=numrides)


def read_file_as_type(filename="Data/ctabus.csv", type_name="dict"):
    tracemalloc.start()
    tracemalloc.clear_traces()

    results = None

    try:
        if type_name == "columns":
            results = read_rides_with_generator(filename)

        if type_name == "generator":
            results = read_rides_as_columns(filename)

        if type_name == "named_tuple":
            results = read_rides_as_tuples(filename)

        elif type_name == "dict":
            results = read_rides_as_dicts(filename)

        elif type_name == "instance":
            results = read_rides_as_instances(filename)

        elif type_name == "slots":
            results = read_rides_as_instances_with_slots(filename)

        else:
            results = read_rides_as_tuples(filename)

        current, peak = tracemalloc.get_traced_memory()

        print(
            f"Memory Use for {type_name}: Current {current}, Peak {format(peak, '08,.1f')}"
        )

    except Exception as e:
        print(e)

    return results


if __name__ == "__main__":

    # for type_name in ["tuple", "named_tuple", "dict", "instance", "slots"]:
    for function_to_call in [
        read_rides_as_tuples,
        read_rides_as_named_tuples,
        read_rides_as_instances,
        read_rides_as_instances_with_slots,
        read_rides_as_dicts,
    ]:
        # read_file_as_type("Data/ctabus.csv", type_name)
        function_to_call("Data/ctabus.csv")

import csv
import tracemalloc
from collections.abc import Sequence
from collections import namedtuple, defaultdict


class DataCollection(Sequence):
    def __init__(self, columns):
        self.column_names = list(columns)
        self.column_data = list(columns.values())

    def __len__(self):
        return len(self.column_data.values()[0])

    def __getitem__(self, key):
        if isinstance(key, slice):
            slicer = DataCollection()
            slicer.column_data = {
                header: data_list[key] for header, data_list in self.column_data.items()
            }
            return slicer
        elif isinstance(key, int):
            return dict(zip(self.column_names, (col[key] for col in self.column_data)))

    def append(self, d):
        for key, val in d.items():
            self.column_data[key].append(val)


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


def read_csv_as_columns(filename, types):
    columns = defaultdict(list)
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        for row in rows:
            for name, func, val in zip(headers, types, row):
                columns[name].append(func(val))

    return DataCollection(columns)


def read_rides_as_data_collection(filename, converters):

    columns = defaultdict(list)

    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        for row in rows:
            for name, func, val in zip(headers, converters, row):
                columns[name].append(func(val))

    return DataCollection(columns)


def read_rides_as_dicts(filename):
    """
    Read the bus ride data as a list of dicts
    """
    records = DataCollection()
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


def read_rides_as_generator(filename):
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


def read_file_as_type(filename="Data/ctabus.csv", type_name="dict", converters=[]):
    tracemalloc.start()
    tracemalloc.clear_traces()

    results = None

    try:

        results = globals()[f"read_rides_as_{type_name}"](filename, converters)

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

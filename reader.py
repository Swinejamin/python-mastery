import csv
import tracemalloc
from collections import defaultdict
from collections.abc import Sequence

from pprint import pprint


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


def read_csv_as_dicts(filename, converter_funcs):

    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)

        converted_values = [
            {name: func(val) for name, func, val in zip(headers, converter_funcs, row)}
            for row in rows
        ]

    return converted_values

def read_csv_as_instances(filename, cls):
    '''
    Read a CSV file into a list of instances
    '''
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        for row in rows:
            records.append(cls.from_row(row))
    return records


def read_file_as_data_collection(filename, converters):
    columns = defaultdict(list)

    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        for row in rows:
            for name, func, val in zip(headers, converters, row):
                columns[name].append(func(val))

    return DataCollection(columns)


def read_file_as_type(filename="Data/ctabus.csv", type_name="dict", converters=[]):
    tracemalloc.start()
    tracemalloc.clear_traces()

    results = None

    try:

        results = globals()[f"read_file_as_{type_name}"](filename, converters)

        current, peak = tracemalloc.get_traced_memory()

        print(
            f"Memory Use for {type_name}: Current {current}, Peak {format(peak, '08,.1f')}"
        )

    except Exception as e:
        print(e)

    return results

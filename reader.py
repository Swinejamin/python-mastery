from pprint import pprint
import csv


def read_csv_as_dicts(filename, converter_funcs):

    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)

        converted_values = [
            {name: func(val) for name, func, val in zip(headers, converter_funcs, row)}
            for row in rows
        ]

    return converted_values

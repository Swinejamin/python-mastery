from readrides import read_file_as_type
from pprint import pprint
from collections import Counter

rows = read_file_as_type(
    "Data/ctabus.csv",
    "dict",
)


# How many bus routes exist in Chicago?
routes = sorted({s["route"] for s in rows})

print(f"Number of routes: {len(routes)}")


# How many people rode the number 22 bus on February 2, 2011? What about any route on any date of your choosing?


def get_riders_by_date(date, data=rows):

    # count = Counter(row["rides"] for row in routes if date == row["date"])
    # pprint(count)
    # for row in data:
    #     if date == row["date"]:
    #         pprint(row)

    try:
        riders = [row for row in data if date == row["date"]]
        count = sum([r["rides"] for r in riders])

        print(
            f'Count: {count}, Revamp: {filter(lambda ride:  ride["date"] ==  date , data)}'
        )

        return {riders: riders, count: count}

    except Exception as e:
        print(f"Oops: {e}")


def get_riders_by_bus_number(route_to_check, data=rows):

    filtered_rows = [row for row in data if route_to_check == row["route"]]
    count = sum([r["rides"] for r in filtered_rows])
    results = {filtered_rows: filtered_rows, count: count}
    return results


print(
    f"Number of riders on February 2, 2011: {get_riders_by_date('02/02/2011')['count']}"
)
print(f"Number of riders on Bus #22: {get_riders_by_bus_number('22')['count']}")

bus22 = get_riders_by_bus_number("22")


print(
    f"Riders on February 2, 2011 on Bus #22: {sum([r['rides'] for r in get_riders_by_date('02/02/2011', get_riders_by_bus_number('22')['filtered_rows'])])}"
)
# What is the total number of rides taken on each bus route?


#
# What five bus routes had the greatest ten-year increase in ridership from 2001 to 2011?

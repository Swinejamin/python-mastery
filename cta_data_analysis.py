from readrides import read_file_as_type, read_rides_as_dicts
import csv
from pprint import pprint
import tracemalloc
from collections import Counter, defaultdict


def solutions():
    from collections import defaultdict, Counter

    rows = read_file_as_type()

    # --------------------------------------------------
    # Question 1:  How many bus routes are in Chicago?
    # Solution: Use a set to get unique values.

    routes = set()
    for row in rows:
        routes.add(row["route"])

    answer1 = len(routes)

    # --------------------------------------------------
    # Question 2: How many people rode route 22 on February 2, 2011?
    # Solution: Make dictionary with composite keys

    by_route_date = {}
    for row in rows:
        by_route_date[row["route"], row["date"]] = row["rides"]

    answer2 = by_route_date["22", "02/02/2011"]

    # --------------------------------------------------
    # Question 3: Total number of rides per route
    # Solution: Use a counter to tabulate things
    rides_per_route = Counter()
    for row in rows:
        rides_per_route[row["route"]] += row["rides"]

    answer3 = list()

    # Make a table showing the routes and a count ranked by popularity
    for route, count in rides_per_route.most_common():
        answer3.append((route, count))

    # --------------------------------------------------
    # Question 4: Routes with greatest increase in ridership 2001 - 2011
    # Solution: Counters embedded inside a defaultdict

    answer4 = list()
    rides_by_year = defaultdict(Counter)

    for row in rows:
        year = row["date"].split("/")[2]
        rides_by_year[year][row["route"]] += row["rides"]

    diffs = rides_by_year["2011"] - rides_by_year["2001"]

    for route, diff in diffs.most_common(5):
        answer4.append((route, diff))

    return {
        "answer1": answer1,
        "answer2": answer2,
        "answer3": answer3,
        "answer4": answer4,
    }


rides_by_route = Counter()
rides_by_year = defaultdict(Counter)
unique_routes = set()
by_route_date = {}

rows = read_file_as_type("Data/ctabus.csv")

for row in rows:
    route, date, daytype, rides = row.values()
    year = date.split("/")[2]

    unique_routes.add(route)

    by_route_date[route, date] = rides

    rides_by_year[year][route] += rides

    rides_by_route[route] += rides

unique_routes = sorted(unique_routes)

answers = solutions()


def check_my_answer(answer, solution):
    if answer == solution:
        print(f"{answer} is correct!")
    else:
        print(f"{answer} is not correct! The correct answer is {solution}")


# How many bus routes exist in Chicago?
myAnswer1 = len(unique_routes)
check_my_answer(myAnswer1, answers["answer1"])


# How many people rode the number 22 bus on February 2, 2011? What about any route on any date of your choosing?
myAnswer2 = by_route_date["22", "02/02/2011"]
check_my_answer(myAnswer2, answers["answer2"])


# What is the total number of rides taken on each bus route?
for index, (route, count) in enumerate(rides_by_route.most_common(10)):
    myAnswer3 = (route, count)
    check_my_answer(myAnswer3, answers["answer3"][index])


# What five bus routes had the greatest ten-year increase in ridership from 2001 to 2011?
diffs = rides_by_year["2011"] - rides_by_year["2001"]

for index, (route, diff) in enumerate(diffs.most_common(5)):
    myAnswer4 = (route, diff)
    check_my_answer(myAnswer4, answers["answer4"][index])

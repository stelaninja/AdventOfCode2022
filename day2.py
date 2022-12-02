"""
Day 2 of Advent Of Code 2022
https://adventofcode.com/2022/
"""
import os
import re
import sys

import requests

SESSION_KEY = {"session": os.environ.get("SESSION_KEY", None)}
DAY = int(re.findall(r"[0-9]", sys.argv[0].rsplit("/", maxsplit=1)[-1])[0])


response = requests.get(
    f"https://adventofcode.com/2022/day/{DAY}/input", cookies=SESSION_KEY, timeout=500
)

data = response.text

win_table = {
    "A": "Y",
    "B": "Z",
    "C": "X"
}

draw_table = {
    "A": "X",
    "B": "Y",
    "C": "Z"
}

lose_table = {
    "A": "Z",
    "B": "X",
    "C": "Y"
}

point_table = {
    "X": 1,
    "Y": 2,
    "Z": 3
}

options = {
    "X": lose_table,
    "Y": draw_table,
    "Z": win_table
}

games = data.strip().split("\n")

points_p1 = 0
points_p2 = 0

for game in games:
    h1, h2 = game.split()
    pt = []
    if win_table[h1] == h2:
        points_p1 += 6
    if draw_table[h1] == h2:
        points_p1 += 3

    points_p1 += point_table[h2]
    points_p2 += point_table[options[h2][h1]] + {"X": 0, "Y":3, "Z": 6}[h2]

# PART 1
print(f"Part 1: {points_p1}")


# PART 2
print(f"Part 2: {points_p2}")
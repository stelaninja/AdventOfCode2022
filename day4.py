"""
Day 4 of Advent Of Code 2022
https://adventofcode.com/2022/
"""
import os
import re
import sys

import requests

SESSION_KEY = {"session": os.environ.get("SESSION_KEY", None)}
DAY = int(re.findall(r"[0-9]+", sys.argv[0].rsplit("/", maxsplit=1)[-1])[0])


response = requests.get(
    f"https://adventofcode.com/2022/day/{DAY}/input", cookies=SESSION_KEY, timeout=500
)

data = response.text.strip().split("\n")
assignments = [x.split(",") for x in data]


contained = 0
overlap = 0

for e1, e2 in assignments:
    e1 = [int(x) for x in e1.split("-")]
    e2 = [int(x) for x in e2.split("-")]

    s1 = set(range(e1[0], e1[1] + 1))
    s2 = set(range(e2[0], e2[1] + 1))

    # PART 1
    if s1 <= s2 or s2 <= s1:
        contained += 1

    # PART 2
    if s1 & s2:
        overlap += 1

print(f"Part 1: {contained}")
print(f"Part 2: {overlap}")

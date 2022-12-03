"""
Day 3 of Advent Of Code 2022
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
data = data.strip().split("\n")


alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

# PART 1
prio_list = []

for rucksack in data:
    comp1, comp2 = rucksack[:len(rucksack) // 2], rucksack[len(rucksack) // 2:]
    diff = set(comp1).intersection(set(comp2))
    prio = alpha.index(list(diff)[0]) + 1
    prio_list.append(prio)

i = 3

print(f"Part 1: {sum(prio_list)}")

# PART 2
badge_list = []
while i <= len(data):
    group = data[i-3:i]
    s1, s2, s3 = [set(x) for x in group]

    i += 3

    badge = s1.intersection(s2.intersection(s3))
    badge_list.append(alpha.index(list(badge)[0]) + 1)

print(f"Part 2: {sum(badge_list)}")


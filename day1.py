"""
Day 1 of Advent Of Code 2022
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


## PART 1 & 2
elf_table = [elf for elf in data.split("\n\n")]
calorie_table = [cals.split("\n") for cals in elf_table[:-1]]
calorie_table = [[int(x) for x in cals] for cals in calorie_table]

sum_table = [sum(x) for x in calorie_table]


print("Part 1:")
print(max(sum_table))

print("Part 2:")
print(sum(sorted(sum_table)[-3:]))
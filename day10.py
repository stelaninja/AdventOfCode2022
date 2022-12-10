"""
Day 10 of Advent Of Code 2022
https://adventofcode.com/2022/
"""
import os
import re
import sys

import numpy as np
import requests

SESSION_KEY = {"session": os.environ.get("SESSION_KEY", None)}
DAY = int(re.findall(r"[0-9]+", sys.argv[0].rsplit("/", maxsplit=1)[-1])[0])


response = requests.get(
    f"https://adventofcode.com/2022/day/{DAY}/input", cookies=SESSION_KEY, timeout=500
)


data = response.text.strip().split("\n")

data = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

data = data.split("\n")
# print(data[:10])

cycles = {}
cycle = 1
x = 1

crt = np.full(240, ".")
clock = 0

# # ---- START: PART 1 WORKING ----
# for operation in data:

#     if operation.startswith("noop"):
#         cycles[cycle] = x
#         cycle += 1
#     else:

#         for _ in range(2):
#             cycles[cycle] = x
#             cycle += 1

#         x += int(operation.split()[1])
#         cycles[cycle] = x
# # ---- START: PART 1 WORKING ----


for operation in data:
    print(cycle, x, operation)

    if operation.startswith("noop"):
        if cycle - 1 < x < cycle + 1:
            crt[cycle] = "#"

        cycles[cycle] = x
        cycle += 1
    else:
        for _ in range(2):
            if cycle % 40 - 1 <= x <= cycle % 40 + 1:
                crt[cycle - 1] = "#"

            cycles[cycle] = x
            cycle += 1

        x += int(operation.split()[1])
        cycles[cycle] = x


signal_strength = 0
cycle_idxs = [20, 60, 100, 140, 180, 220]

for i in cycle_idxs:
    signal_strength += i * cycles.get(i)

print(f"Part 1: {signal_strength}")


crt = crt.reshape(6, 40)
# print(crt)
for row in crt:
    print("".join(row))

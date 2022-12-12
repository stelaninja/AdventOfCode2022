"""
Day 11 of Advent Of Code 2022
https://adventofcode.com/2022/
"""
import copy
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


data = response.text.strip().split("\n\n")

# data = """Monkey 0:
#   Starting items: 79, 98
#   Operation: new = old * 19
#   Test: divisible by 23
#     If true: throw to monkey 2
#     If false: throw to monkey 3

# Monkey 1:
#   Starting items: 54, 65, 75, 74
#   Operation: new = old + 6
#   Test: divisible by 19
#     If true: throw to monkey 2
#     If false: throw to monkey 0

# Monkey 2:
#   Starting items: 79, 60, 97
#   Operation: new = old * old
#   Test: divisible by 13
#     If true: throw to monkey 1
#     If false: throw to monkey 3

# Monkey 3:
#   Starting items: 74
#   Operation: new = old + 3
#   Test: divisible by 17
#     If true: throw to monkey 0
#     If false: throw to monkey 1"""

# data = data.split("\n\n")

monkies = {}

for monkey in data:
    # print(monkey, "\n")
    l = monkey.split("\n")

    n = re.findall("[0-9]", l[0])[0]
    start_items = re.findall("[0-9]+", l[1])
    operation = re.findall(": new = old (.+)", l[2])[0]
    # test = re.findall(": (.+)", l[3])[0]
    test = re.findall("[0-9]+", l[3])[0]
    if_true = re.findall("[0-9]", l[4])[0]
    if_false = re.findall("[0-9]", l[5])[0]
    monkies[n] = {
        "start_items": start_items,
        "operation": operation,
        "test": test,
        "if_true": if_true,
        "if_false": if_false,
        "times_inspected": 0,
    }

# print(monkies["0"])


def play_round(monkey_dict, part, counter):
    for monkey in monkey_dict:
        # print("Starting monkey", monkey)
        for item in monkey_dict[monkey]["start_items"]:
            counter += 1
            if counter % 1000 == 0:
                print("Iteration", counter)
            old = int(item)
            monkey_dict[monkey]["times_inspected"] += 1
            # print("Inspecting:", old)
            worry = eval(f"{str(old)} {monkey_dict[monkey]['operation']}")
            if part == "p1":
                worry = worry / 3

            worry = worry // 1

            if worry % int(monkey_dict[monkey]["test"]) == 0:
                # print(monkey_dict[monkey_dict[monkey]["if_true"]]["start_items"])
                monkey_dict[monkey_dict[monkey]["if_true"]]["start_items"].append(
                    int(worry)
                )
            else:
                monkey_dict[monkey_dict[monkey]["if_false"]]["start_items"].append(
                    int(worry)
                )

            # print(monkey_dict[monkey])
        monkey_dict[monkey]["start_items"] = []

    return counter


# PART 1
m_1 = copy.deepcopy(monkies)

for _ in range(20):
    play_round(m_1, "p1")

mb1, mb2 = sorted([v["times_inspected"] for k, v in m_1.items()])[-2:]
print("Part 1:", mb1 * mb2)


# PART 2
m_2 = copy.deepcopy(monkies)
counter = 0
for i in range(10000):
    print(i)
    counter = play_round(m_2, "p2", counter)
mb1, mb2 = sorted([v["times_inspected"] for k, v in monkies.items()])[-2:]
print("Part 1:", mb1 * mb2)

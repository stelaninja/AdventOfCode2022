"""
Day 5 of Advent Of Code 2022
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

data = response.text  # .strip().split("\n")
stacks, moves = data.split("\n\n")
moves = moves.strip()
stack_table = {
    i: [] for i in range(1, max([int(x) for x in re.findall("[0-9]+", stacks)]) + 1)
}

for line in stacks.split("\n")[:-1]:
    for i in range(len(line) - 1):
        if i >= len(stack_table):
            break
        search_range = line[i * 4 : i * 4 + 4]
        if re.search("[A-Z]", search_range):
            stack_table[i + 1].append(
                search_range.replace(" ", "").replace("[", "").replace("]", "")
            )


def move_crates(s_table, max_move_size=False):
    """
    Moves the crates

    Args:
        s_table (dict): Dictonary with stacks
        max_move_size (bool, optional): If True only move one crate per moves. Defaults to False.

    Returns:
        dict: Dictionary of stacks
    """
    st = {}
    for k, v in s_table.items():
        st[k] = v[:]

    for move in moves.split("\n"):
        num_to_move = int(re.findall("move ([0-9]+)", move)[0])
        from_stack = int(re.findall("from ([0-9]+)", move)[0])
        to_stack = int(re.findall("to ([0-9]+)", move)[0])

        if max_move_size:
            for _ in range(num_to_move):
                st[to_stack].insert(0, st[from_stack].pop(0))
            st[to_stack] = [x for y in st[to_stack] for x in y]

        else:
            st[to_stack].insert(0, st[from_stack][:num_to_move])
            del st[from_stack][:num_to_move]

            st[to_stack] = [x for y in st[to_stack] for x in y]

    return st


# PART 1
p1_stack = move_crates(stack_table, True)
p1 = []
for stack in p1_stack.items():
    p1.append(stack[1][0])

print(f"Part 1: {''.join(p1)}")

# PART 2
p2_stack = move_crates(stack_table, False)
p2 = []
for stack in p2_stack.items():
    p2.append(stack[1][0])
print(f"Part 2: {''.join(p2)}")

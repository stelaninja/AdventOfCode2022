"""
Day 8 of Advent Of Code 2022
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


# data = """30373
# 25512
# 65332
# 33549
# 35390""".split(
#     "\n"
# )

data = np.array([[int(y) for y in x] for x in data])
visible_map = np.zeros(data.shape)


def look_for_trees(data_arr, map_arr):
    """Looks for trees in the array

    Args:
        data_arr (np.array): Input array with trees.
        map_arr (np.array): Map of where there are visible trees.

    Returns:
        _type_: _description_
    """
    for i, row in enumerate(data_arr):
        highest = row[0]
        map_arr[i, 0] = 1

        for j, c in enumerate(row):
            if c > row[j - 1] and c > highest:
                if not j == 0:
                    map_arr[i, j] = 1
                    highest = max(highest, c)
    return map_arr


visible_map = look_for_trees(data, visible_map)
visible_map = look_for_trees(np.flip(data, 1), np.flip(visible_map, 1))
visible_map = look_for_trees(data.T, np.flip(visible_map, 1).T)
visible_map = look_for_trees(np.flip(data.T, 1), np.flip(visible_map, 1))

visible_map = np.flip(visible_map, 1)

print(f"Part 1: {int(np.sum(visible_map))}")

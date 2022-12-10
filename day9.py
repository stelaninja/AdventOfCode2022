"""
Day 9 of Advent Of Code 2022
https://adventofcode.com/2022/
"""
import os
import re
import sys

import numpy as np
import requests

SESSION_KEY = {"session": os.environ.get("SESSION_KEY", None)}
DAY = int(re.findall(r"[0-9]", sys.argv[0].rsplit("/", maxsplit=1)[-1])[0])


response = requests.get(
    f"https://adventofcode.com/2022/day/{DAY}/input", cookies=SESSION_KEY, timeout=500
)


data = response.text.strip().split("\n")

data = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2""".split(
    "\n"
)

# print(data)


# np.set_printoptions(threshold=sys.maxsize, linewidth=size_x * 5)


max_x, min_x, max_y, min_y = 0, 0, 0, 0
curr_x, curr_y = 0, 0

for line in data:
    direction, steps = line.split()
    steps = int(steps)
    if direction == "U":
        curr_y += steps
    elif direction == "D":
        curr_y -= steps
    elif direction == "R":
        curr_x += steps
    elif direction == "L":
        curr_x -= steps

    if curr_y > max_y:
        max_y = curr_y
    elif curr_y < min_y:
        min_y = curr_y
    if curr_x > max_x:
        max_x = curr_x
    elif curr_x < min_x:
        min_x = curr_x


print(f"X: {curr_x}, {min_x}-{max_x}")
print(f"Y: {curr_y}, {min_y}-{max_y}")

size_y = abs(min_y) + max_y + 1
size_x = abs(min_x) + max_x + 1
print(size_y, size_x)
origin = (size_y - abs(min_y) - 1, abs(min_x))
print(origin)
# sys.exit()


class Array:
    def __init__(self, fill, type_):
        self.arr = np.full((size_y, size_x), fill)
        self.curr_pos = origin
        self.fill = fill
        self.type_ = type_

        # self.arr[size_y - 1, 0] = type_
        # print(self.arr)
        self.arr[origin] = type_
        self.direction_func = {
            "U": self.up,
            "D": self.down,
            "L": self.left,
            "R": self.right,
        }

    def up(self):
        self.arr[self.curr_pos] = self.fill
        # self.curr_pos = (self.curr_pos[0] - 1) % size_y, self.curr_pos[1]
        self.curr_pos = (self.curr_pos[0] - 1), self.curr_pos[1]
        # print(self.curr_pos)
        self.arr[self.curr_pos] = self.type_

    def down(self):
        self.arr[self.curr_pos] = self.fill
        # self.curr_pos = (self.curr_pos[0] + 1) % size_y, self.curr_pos[1]
        self.curr_pos = (self.curr_pos[0] + 1), self.curr_pos[1]
        # print(self.curr_pos)
        self.arr[self.curr_pos] = self.type_

    def left(self):
        self.arr[self.curr_pos] = self.fill
        # self.curr_pos = self.curr_pos[0], (self.curr_pos[1] - 1) % size_x
        self.curr_pos = self.curr_pos[0], (self.curr_pos[1] - 1)
        # print(self.curr_pos)
        self.arr[self.curr_pos] = self.type_

    def right(self):
        if self.curr_pos[1] > 450:
            print(self.curr_pos)
        self.arr[self.curr_pos] = self.fill
        # self.curr_pos = self.curr_pos[0], (self.curr_pos[1] + 1) % size_x
        self.curr_pos = self.curr_pos[0], (self.curr_pos[1] + 1)
        # print(self.curr_pos)
        self.arr[self.curr_pos] = self.type_

    def __repr__(self) -> str:
        return np.array_repr(self.arr)


head_arr = Array("X", "H")
tail_arr = Array("X", "T")
count_arr = Array(0, 1)


for move in data:
    direction, steps = move.split()
    for _ in range(int(steps)):
        view_arr = np.full((size_y, size_x), ".")
        # for arr in [head_arr]:  # , tail_arr, count_arr]:
        head_arr.direction_func[direction]()
        y_diff = abs(tail_arr.curr_pos[0] - head_arr.curr_pos[0])
        y_dir = tail_arr.curr_pos[0] - head_arr.curr_pos[0]
        x_diff = abs(tail_arr.curr_pos[1] - head_arr.curr_pos[1])
        x_dir = head_arr.curr_pos[0] - tail_arr.curr_pos[0]

        if (y_diff > 1 and x_diff > 0) or (y_diff > 0 and x_diff > 1):
            if direction in ["U", "D"]:
                add_dir = "L" if x_dir > 0 else "R"
            else:
                add_dir = "U" if x_dir < 0 else "D"
            tail_arr.direction_func[direction]()
            tail_arr.direction_func[add_dir]()
        elif y_diff > 1 or x_diff > 1:
            tail_arr.direction_func[direction]()

        count_arr.arr[tail_arr.curr_pos] = 1
        view_arr[head_arr.curr_pos] = "H"
        view_arr[tail_arr.curr_pos] = "T"

        # print(view_arr)


# print(head_arr)
# head_arr.up()
# print(head_arr)
print(count_arr)
print(np.sum(count_arr.arr))

# PART 1: 2812 to low, 7404 too high, 7160 too high

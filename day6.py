"""
Day 6 of Advent Of Code 2022
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

data = response.text.strip()

marker_length = {
    "packet": 4,
    "message": 14,
}

for part, marker_type in zip(range(1, 3), ["packet", "message"]):
    marker = False
    m_len = marker_length[marker_type]
    idx = m_len - 1

    while not marker:
        idx += 1
        if len(set(data[idx - m_len : idx])) == m_len:
            marker = True

    print(f"Part {part}: {idx}")

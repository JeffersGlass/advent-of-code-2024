import re

first, second = list(), list()
pattern = re.compile(r"(\d+)\s+(\d+)")

with open("day1/data.txt", "r") as f:
    for line in f.readlines():
        m = re.match(pattern, line.strip())
        a, b = m.group(1), m.group(2)
        first.append(int(a))
        second.append(int(b))

first.sort()
second.sort()

print(f"Result: {sum(abs(int(d[0])-int(d[1])) for d in zip(first, second))}")
from collections import Counter
import re

first, second = Counter(), Counter()
pattern = re.compile(r"(\d+)\s+(\d+)")

with open("day1/data.txt", "r") as f:
    for line in f.readlines():
        m = re.match(pattern, line.strip())
        if not m: continue
        a, b = m.group(1), m.group(2)
        first.update([(int(a))])
        second.update([(int(b))])

total = 0
for num in first:
    total += num * second[num]

print(f"Result: {total}")
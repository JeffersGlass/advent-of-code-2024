import bisect
import re

with open("day3/data.txt", "r") as f:
    # Since the data starts "enabled", prepend a "do()" command
    data = "do()" + f.read()

# Find all the 
mul_pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
muls = re.finditer(mul_pattern, data)

do_pattern = re.compile(r"do\(\)")
dont_pattern = re.compile(r"don't\(\)")
dos = sorted(m.span()[0] for m in re.finditer(do_pattern, data))
donts = sorted(m.span()[0] for m in re.finditer(dont_pattern, data))

total = 0
for m in muls:
    start = m.span()[0]

    # Find the index of the preceding "do()" and "dont't()"
    nearest_do = bisect.bisect_right(dos, start)
    nearest_dont = bisect.bisect_right(donts, start)

    # If we haven't seen a don't, or the last highest do is closer than
    # the last highest don't, add to total. We don't need to check if
    # nearest_do() is 0, since we've inserted a do() at the very beginning
    # of our data
    if nearest_dont == 0 or (dos[nearest_do-1] > donts[nearest_dont-1]):
        total += int(m.group(1)) * int(m.group(2))

print(f"{total=}")

    
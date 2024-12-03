import re

with open("day3/data.txt", "r") as f:
    data = f.read()

pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
muls = re.findall(pattern, data)
print(f"Total: {sum(int(m[0]) * int(m[1]) for m in muls)}")
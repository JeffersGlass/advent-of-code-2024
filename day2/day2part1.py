from itertools import pairwise

with open("day2/data.txt", "r") as f:
    data = ((int(x) for x in line.split(" ")) for line in f.readlines())

safe_reports = 0
for report in data:
    dir = 0
    valid = True
    for prev, next in pairwise(report):
        if dir * (next-prev) < 0: valid = False; break
        dir = next - prev

        if not 1 <= abs(prev - next) <= 3: valid = False; break

    if valid: safe_reports += 1

print(f"Safe resports: {safe_reports}")
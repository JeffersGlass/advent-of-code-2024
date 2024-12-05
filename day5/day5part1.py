from collections import defaultdict
import re

with open("day5/data.txt", "r") as f:
    raw_data = f.read()

raw_rules, raw_updates = raw_data.split("\n\n")
raw_rules = raw_rules.split("\n")
updates = [line.split(",") for line in raw_updates.split("\n")]

rules = defaultdict(set)

rules_pattern = re.compile(r"(\d+)\|(\d+)")
for line in raw_rules:
    m = re.match(rules_pattern, line.strip())
    rules[m.group(1)].add(m.group(2))

total = 0
for update in updates:
    valid = True
    for i, first in enumerate(update[:-1]):
        for second in update[i+1:]:
            if not second in rules[first]:
                valid = False
                break
        if not valid: break
    if valid:
        total += int(update[int((len(update)-1)/2)])

print(f"{total= }")

    



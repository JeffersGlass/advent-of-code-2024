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


class SortWrapper:
    rules = rules
    
    def __init__(self, s: str):
        self.s = s
        

    def __lt__(self, other):
        return other.s in self.rules[self.s]

    def __int__(self) -> int:
        return int(self.s)

total = 0
for update in updates:
    valid = True
    for i, first in enumerate(update[:-1]):
        for second in update[i+1:]:
            if not second in rules[first]:
                valid = False
                break
        if not valid: break
    if not valid:
        update = [int(u) for u in sorted([SortWrapper(s) for s in update])]
        total += update[int((len(update)-1)/2)]

print(f"{total= }")

    



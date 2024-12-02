from itertools import pairwise

def check_report_with_excise(report: list[int]) -> bool:
    return is_report_safe(report) or any((is_report_safe(excise(report, i)) for i in range(len(report))))

def excise(s: list[int], index: int) -> list[int]:
    if index == len(s): return s[:-1]
    return s[:index] + s[index+1:]

def is_report_safe(report: list[int], level = 1) -> bool:
    if level < 0: return False

    dir = 0
    valid = True
    for prev, next in pairwise(enumerate(report)):
        prev_val, next_val = prev[1], next[1]
        if dir * (next_val-prev_val) < 0: valid = False; break

        dir = next_val - prev_val

        if not 1 <= abs(prev_val - next_val) <= 3: valid = False; break

    if valid: return True
    return False

if __name__ == "__main__":
    with open("day2/data.txt", "r") as f:
        data = [[int(x) for x in line.split(" ")] for line in f.readlines()]

    print(f"Result: {[check_report_with_excise(r) for r in data].count(True)}")
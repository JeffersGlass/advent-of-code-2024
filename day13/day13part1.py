from pathlib import Path
import re
from typing import NamedTuple, cast
from sympy import symbols, init_printing, solve

Machine = NamedTuple('Machine', [('ax', int), ('ay', int), ('bx', int), ('by', int), ('px', int), ('py', int)])

def load_data_from_path(p: str | Path, is_part_2 = False)-> list[Machine] : 
    with open(p, "r") as f:
        sections = f.read().split("\n\n")
    
    machines: list[Machine] = []
    for s in sections:
        a, b, prize = s.split("\n")
        ax, ay = (m:= cast(re.Match, re.match(r"Button A: X\+(\d+), Y\+(\d+)", a))).group(1), m.group(2)
        bx, by = (m:= cast(re.Match, re.match(r"Button B: X\+(\d+), Y\+(\d+)", b))).group(1), m.group(2)
        px, py = (m:= cast(re.Match, re.match(r"Prize: X=(\d+), Y=(\d+)", prize))).group(1), m.group(2)
        if is_part_2: 
            px = int(px) + 10000000000000
            py = int(py) + 10000000000000
        machines.append(Machine(ax=int(ax), ay=int(ay), bx=int(bx), by=int(by), px=int(px), py=int(py)))

    return machines

def solve_machine(m: Machine) -> tuple[int, int] | None:
    A, B = symbols("A B")
    result: dict = solve([A*m.ax + B*m.bx - m.px, A*m.ay + B*m.by - m.py], [A, B], dict=True)
    if int(result[0][A]) == result[0][A] and int(result[0][B]) == result[0][B]:
        return int(result[0][A]), int(result[0][B])
    else:
        return None
    
def score_machine(m: Machine) -> int:
    if r:= solve_machine(m):
        return 3*r[0] + r[1]
    return 0




if __name__ == "__main__":
    init_printing(use_unicode=True)
    data = load_data_from_path("day13/data.txt", is_part_2=True)
    print(sum(score_machine(m) for m in data))
    

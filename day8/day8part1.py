from collections import defaultdict
import itertools
import string
from typing import NamedTuple

VISUALIZE = False

if VISUALIZE:
    from rich import print

Position = NamedTuple("Position", [('line', int), ('char', int)])

class AntennaMap:
    def __init__(self, data: list[str] | None = None):
        self.antennas: dict[str, set[Position]] | None = None
        self.num_lines = -1
        self.num_chars = -1
        self.initialized = False

        if data: self.load_data(data)
        self.initialized = True
                             
    def load_data(self, raw: list[str]) -> None:
        antennas: dict[str, set[Position]] = defaultdict(set)
        for l, line in enumerate(raw):
            for c, char in enumerate(line.strip()):
                if char.isalnum(): antennas[char].add(Position(int(l), int(c)))
        self.antennas = antennas
        self.num_lines = len(raw)
        self.num_chars = len(raw[0].strip())
        self.initialized = True

    def inbound(self, l, c):
        return 0 <= l < self.num_lines and 0 <= c < self.num_chars

    def calc_antinodes(self, label: str) -> set[Position]:
        results = set()
        if not self.antennas: raise ValueError("Tried to calculate antinodes before initializing antennas")
        antenna_set = self.antennas[label]
        # TODO maybe try this with itertools.permutations and one diff instead of combinations and two?g``
        for first, second in itertools.combinations(antenna_set, 2):
            diff = Position(second.line - first.line, second.char - first.char)
            options = (
                    (second.line + diff.line, second.char + diff.char),
                    (first.line - diff.line, first.char - diff.char)
                    )
            for pos in options:
                if self.inbound(*pos):
                    results.add(pos)
        return results

    def calc_all_antinodes(self) -> set[Position]:
        results = set()
        if self.antennas is None: raise ValueError("Tried to calculate antinodes before initializing antennas")
        for name in sorted(self.antennas):
            res = self.calc_antinodes(name)
            print(name, res)
            results |=  res
        return results

    def vis(self, locations: set[Position], res: set[Position], name: str, max_line:int , max_char:int):
        if not VISUALIZE: return
        for line in range(max_line):
            for char in range(max_char):
                if (line, char) in locations:
                    if (line, char) in res:
                        print(f"[green]{name}[/green]", end = "")
                    else:
                        print(name, end = "")
                else:
                    if (line, char) in res:
                        print(f"[green]#[/green]", end = "")
                    else:
                        print(".", end = "")
            print("")

if __name__ == "__main__":
    
    with open("day8/dataabc.txt", "r") as f:
        ant = AntennaMap(data=f.readlines())

    print(f"{ant.num_lines=} {ant.num_chars=}")
    ant.calc_all_antinodes()
    exit()
    results = set()
    print(f"{num_lines=}, {num_chars=}")
    for name, locations in sorted(antennas.items()):
        res = calc_antinodes(locations, num_lines, num_chars)
        if VISUALIZE:
            print(f"Antenna {name} has antennas at {sorted(locations)}\n and {len(res)} antinodes at {sorted(res)}")
            vis(locations, res, name, num_lines, num_chars)
            input()
        results |=  res

    print(f"{len(results)= }")

    

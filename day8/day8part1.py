from collections import defaultdict
import itertools

type Position = tuple[int, int]

_ = defaultdict()

def load_data(raw: list[str]) -> tuple[dict[Position: set], Position, int, int]:
    antennas: dict[str, set[Position]] = defaultdict(set)
    for l, line in enumerate(raw):
        for c, char in enumerate(line.strip()):
            if char != '.': antennas[char].add((int(l), int(c)))
    return antennas, len(raw), len(raw[0])

def inbound(l, c, max_line, max_chars):
    return 0 <= l < max_line and 0 <= c < max_chars

def calc_antinodes(antenna_set: set[Position], max_line, max_char) -> set[Position]:
    results = set()
    for first, second in itertools.combinations(antenna_set, 2):
        diff = (second[0] - first[0], second[1] - first[1])
        options = (
                (second[0] + diff[0], second[1] + diff[1]),
                (first[0] - diff[0], first[1] - diff[1])
                   )
        for pos in options:
            if inbound(*pos, max_line, max_char):
                results.add(pos)
    return results

if __name__ == "__main__":
    with open("day8/data.txt", "r") as f:
        antennas, num_lines, num_chars = load_data(f.readlines())

    results = set()
    for locations in antennas.values():
        results |= calc_antinodes(locations, num_lines, num_chars) 

    print(f"{len(results)= }")

    

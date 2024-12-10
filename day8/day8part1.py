from collections import defaultdict
import itertools

VISUALIZE = True

if VISUALIZE:
    import rich

type Position = tuple[int, int]

def load_data(raw: list[str]) -> tuple[dict[str, set[Position]], int, int]:
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

def vis(locations: set[Position], res: set[Position], name: str, max_line:int , max_char:int):
    for line in range(max_line):
        for char in range(max_char):
            if (line, char) in locations:
                print(name, end = "")
            else:
                print(".", end = "")
        print("")

if __name__ == "__main__":
    with open("day8/data.txt", "r") as f:
        antennas, num_lines, num_chars = load_data(f.readlines())

    results = set()
    print(f"{num_lines=}, {num_chars=}")
    for name, locations in sorted(antennas.items()):
        res = calc_antinodes(locations, num_lines, num_chars)
        print(f"Antenna {name} has antinodes at {res}")
        vis(locations, res, name, num_lines, num_chars)
        input()
        results |=  res

    print(f"{len(results)= }")

    

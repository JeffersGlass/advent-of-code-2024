from collections import UserDict
from pathlib import Path

type TopoData =  dict[tuple[int, int], int]

class TopoMap(UserDict):
    def __init__(self, max_lines:int, max_chars:int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_lines = max_lines
        self.max_chars = max_chars

    @classmethod
    def from_path(cls, p: str | Path):
        with open(p, "r") as f:
            data = f.readlines()

        topo = dict()

        for l, line in enumerate(data):
            for c, char in enumerate(line.strip()):
                if char == ".": topo[(l, c)] = -1
                else: topo[(l, c)] = int(char)
            
        return cls(len(data), len(data[0].strip()), topo)

    def __str__(self):
        return "\n".join("".join(str(self.data[(l, c)]) if self.data[(l, c)] >= 0 else "." for c in range(self.max_chars)) for l in range(self.max_lines))
    
    def inbounds(self, l: int, c: int):
        return 0 <= l < self.max_lines and 0 <= c < self.max_chars
    
    def neighbors(self, l: int, c: int) -> set[tuple[int, int]]:
        results: set[tuple[int, int]] = set()
        for pos in ((l + 1, c), (l - 1, c), (l, c + 1), (l, c - 1)):
            if self.inbounds(*pos): results.add(pos)
        return results

def score_trailhead(topo: TopoMap, l: int, c: int) -> int:
    #print(f"\n\n===Scoring trailhead at {l, c}===")
    assert topo[(l, c)] == 0

    peaks_reached: set[tuple[int, int]] = set()

    endpoints = [(l, c)]
    while endpoints:
        e = endpoints.pop()
        #print(f"Examining endpoint {e} : {topo[e]}")
        for n in (x for x in topo.neighbors(*e) if topo.inbounds(*x)):
            #print(f"\tExamining neighbor {n} : {topo[n]}")
            if topo[n] == topo[e] + 1:
                if topo[n] == 9: 
                    peaks_reached.add(n)
                    #print(f"\t\tFound a peak at {n}")
                else:
                    #print(f"\t\tAdding {n} as new endpoint")
                    if n not in endpoints: endpoints.append(n)
        #print(f"\tEndpoints: {endpoints}")

    return len(peaks_reached)

    
def score_all(topo: TopoMap) -> int:
    zeroes: set[tuple[int, int]] = {(l, c) for (l, c) in topo if topo[(l, c)] == 0}
    return sum(score_trailhead(topo, l, c) for (l, c) in zeroes)

if __name__ == "__main__":
    t = TopoMap.from_path("day10_again/data.txt")
    print(f"{score_all(t)=}")
    print(t)

from collections import UserDict
from collections.abc import Container, Sized, Iterable, Hashable, MutableSet
from itertools import chain
from operator import itemgetter
from pathlib import Path
from typing import Iterator, Self, Generator, Iterable, Any
from functools import cached_property

class Side(MutableSet, Hashable):
    def __init__(self, initial_value: Iterable | None = None):
        self.segments: set[tuple[float, float]] = set()
        if initial_value is not None: self.segments = set(initial_value)

    def __str__(self) -> str:
        return f"Side: {self.segments}"

    def __contains__(self, x: object) -> bool:
        return self.segments.__contains__(x)
    
    def __len__(self):
        return len(self.segments)
    
    def __iter__(self):
        return iter(self.segments)
    
    def __hash__(self):
        return id(self)
    
    def add(self, value: Any) -> None:
        return self.segments.add(value)
    
    def discard(self, value: Any) -> None:
        return self.segments.discard(value)

    def matches(self, seg: tuple[float, float]) -> bool:
        if seg in self.segments: return True
        for delta in -1, 1:
            other = (seg[0], seg[1] + delta)
            if seg[1] == int(seg[1]) and other in self.segments: return True
        for delta in -1, 1:
            other = (seg[0] + delta, seg[1])
            if seg[0] == int(seg[0]) and other in self.segments: return True
        return False
    
def test_side():
    s = Side([(1, 2.5)])
    assert s.matches((1,2.5))
    assert not s.matches((1,3.5))
    assert s.matches((2, 2.5))

    t = Side([(0.5, 0)])
    assert t.matches((0.5, 0))
    assert not t.matches((1.5, 0))
    assert t.matches((0.5, 1))


class Region(Container, Sized, Iterable, Hashable):
    def __init__(self, label: str, positions: Iterable[tuple[int, int]] | None = None):
        self.label = label
        self.sides: set[Side] = set()

        if positions: self.positions = set(positions)
        else: self.positions = set()

    def __str__(self) -> str:
        return f"<Region Label:{self.label} Area:{self.area}>"

    def __contains__(self, x: object) -> bool:
        return x in self.positions
    
    def __len__(self) -> int:
        return len(self.positions)

    def __iter__(self) -> Iterator:
        return self.positions.__iter__()
    
    def __hash__(self) -> int:
        return id(self)
    
    def add(self, o:tuple[int, int]):
        self.positions.add(o)

    def remove(self, o:tuple[int, int]):
        self.positions.remove(o)

    @property
    def area(self) -> int:
        return len(self)
    
    @property
    def num_sides(self) -> int:
        self.sides = set()
        for seg in self.side_segments():
            found_match = False
            for side in self.sides:
                if side.matches(seg):
                    #print(f"Adding segment {seg} to side {side}")
                    side.add(seg)
                    found_match = True
                    #break
            if not found_match:
                #print(f"Starting new side with seg {seg}")
                self.sides.add(Side([seg]))

        print("\n".join(str(s) for s in self.sides))
        return len(self.sides)
    
    def side_segments(self) -> Generator[tuple[float, float]]:
        for p in self:
            for n in Map.neighbors_unrestricted(p):
                if n not in self:
                    yield ((p[0]+n[0])/2, (p[1]+n[1])/2)
    
    def price_in_map(self, map: "Map") -> int:
        return self.area * self.num_sides
    
def test_region():
    r = Region("a", [(0, 0)])
    assert r.area == 1
    assert r.num_sides == 4
    s = Region("b", [(0, 0), (0, 1)])
    assert s.area == 2
    assert s.num_sides == 4
    t = Region("c", [(0,0), (0, 1), (1,0)])
    assert t.area == 3
    assert t.num_sides == 6
    
    

class Map(UserDict):
    def __init__(self, max_lines:int, max_chars:int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_lines = max_lines
        self.max_chars = max_chars
        self._regions: dict[tuple[int, int], Region] = self.init_regions(self.data)
        
    
    @classmethod
    def from_path(cls, s: str | Path) -> Self:
        with open(s, "r") as f:
            data = f.readlines()

        topo: dict[tuple[int, int], str] = dict()

        for l, line in enumerate(data):
            for c, char in enumerate(line.strip()):
                topo[(l, c)] = char
            
        return cls(len(data), len(data[0].strip()), topo)
    

    def __str__(self):
        return "\n".join("".join(str(self.data[(l, c)]) for c in range(self.max_chars)) for l in range(self.max_lines))
    
    def inbounds(self, location: tuple[int, int]):
        l, c = location
        return 0 <= l < self.max_lines and 0 <= c < self.max_chars
    
    @staticmethod
    def neighbors_unrestricted(location) -> Generator[tuple[int, int]]:
        l, c = location
        for pos in ((l + 1, c), (l - 1, c), (l, c + 1), (l, c - 1)):
            yield pos
    
    def neighbors(self, location: tuple[int, int]) -> Generator[tuple[int, int]]:
        l, c = location
        for pos in ((l + 1, c), (l - 1, c), (l, c + 1), (l, c - 1)):
            if self.inbounds(pos): yield pos

    @property
    def regions(self) -> set[Region]:
        return set(self._regions.values())

    
    def init_regions(self, data: dict[tuple[int, int], str]) -> dict[tuple[int, int], Region]:
        to_consider: list[tuple[int, int]] = [(0, 0)]
        first_region = Region(data[(0,0)], [(0, 0)])

        regions: dict[tuple[int, int], Region] = dict()
        regions[(0, 0)] = first_region


        while to_consider:
            if not len(to_consider) % 100: print(f"{len(to_consider)=}")
            cell = to_consider.pop()

            #For debugging; this will get pretty slow
            #assert not any(cell in r for r in regions)
            
            for n in self.neighbors(cell):
                #Looking at a neighbor who already has a region
                if n in regions:
                    if data[n] == data[cell]: #and it matches current cell's label
                        new_region = Region(data[n], regions[n].positions | regions[cell].positions)
                        to_update = list(chain(regions[n].positions, regions[cell].positions))
                        for location in to_update:
                            regions[location] = new_region
                    else: # A non-matching neighbor that already has a region
                        continue
                        

                #Looking at a neighbor not yet in a region
                else:
                    # if the label matches our region, add it to our region
                    if data[cell] == data:
                        regions[n] = regions[cell]
                        regions[n].add(n)
                    else: #otherwise, start a new region
                        regions[n] = Region(data[n], [n])
                    to_consider.append(n)

        return regions


if __name__ == "__main__":
    myMap = Map.from_path("day12/datatest.txt")
    #print(myMap)
    for r in myMap.regions:
        print(f"{r} Num_Sides:{r.num_sides}")# Price:{r.price_in_map(myMap)}")
    print(f"Total cost: {sum(r.price_in_map(myMap) for r in myMap.regions)}")
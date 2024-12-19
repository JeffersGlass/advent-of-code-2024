from collections import UserDict
from collections.abc import Container, Sized, Iterable, Hashable
from itertools import chain
from pathlib import Path
from typing import Iterator, Self, Generator, Iterable

class Region(Container, Sized, Iterable, Hashable):
    def __init__(self, label: str, positions: Iterable[tuple[int, int]] | None = None):
        self.label = label

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
    def perimeter(self) -> int:
        total = 0
        for p in self.positions:
            for n in Map.neighbors_unrestricted(p):
                if n not in self:  
                    total += 1

        return total
    
    def price_in_map(self, map: "Map") -> int:
        return self.area * self.perimeter


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
    myMap = Map.from_path("day12/data.txt")
    print(myMap)
    print("\n".join(f"{r} Perimeter:{r.perimeter} Price:{r.price_in_map(myMap)}" for r in myMap.regions))
    print(f"Total cost: {sum(r.price_in_map(myMap) for r in myMap.regions)}")
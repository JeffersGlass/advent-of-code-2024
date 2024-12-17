from collections import UserDict, deque, defaultdict
from collections.abc import Container, Sized, Iterable, Hashable, MutableSet
from itertools import chain, combinations
from operator import itemgetter
from pathlib import Path
from typing import Iterator, Self, Generator, Iterable, Any
from functools import cached_property
from typing import cast

class Segment(Hashable):
    def __init__(self, segment: tuple[float, float], regions: tuple["Region", "Region"]):
        self.segment = segment
        self.regions = set(regions)

    def __eq__(self, other: object) -> bool:
        if type(other) != Self: return False
        other = cast(Self, other)
        return self.segment == other.segment and self.regions == other.regions
    
    def __hash__(self) -> int:
        return id(self)
    
    def __str__(self) -> str:
        return f"<Segment: {str(self.segment)} Regions: {",".join(r.label for r in self.regions)}"
    
    def matches(self, other: Self) -> bool:
        if self == other: return True
        if self.regions != other.regions: return False

        if self.segment[0] == int(self.segment[0]): # Like (1, 2.5)
            assert self.segment[1] != int(self.segment[1])
            for delta in -1.0, 1.0:
                if (self.segment[0] + delta, self.segment[1]) == other.segment: return True
        elif self.segment[1] == int(self.segment[1]): # (like 0.5, 2)
            assert self.segment[0] != int(self.segment[0])
            for delta in -1.0, 1.0:
                if (self.segment[0], self.segment[1] + delta) == other.segment: return True

        return False

class Side(MutableSet, Hashable):
    def __init__(self, initial_value: Iterable | None = None, borders: Iterable["Region"] | None = None):
        self.segments: set[Segment] = set()
        if initial_value is not None: self.segments = set(initial_value)

        self.borders: list[Region] = list()
        if borders is not None: self.borders = list(borders)

    def __str__(self) -> str:
        return f"Side: {",".join(str(s) for s in self.segments)}"

    def __contains__(self, x: object) -> bool:
        return self.segments.__contains__(x)
    
    def __len__(self):
        return len(self.segments)
    
    def __iter__(self):
        return iter(self.segments)
    
    def __hash__(self):
        return hash(sum(id(t) for t in self.segments))
    
    def add(self, value: Segment) -> None:
        return self.segments.add(value)
    
    def discard(self, value: Segment) -> None:
        return self.segments.discard(value)
    
    def __eq__(self, other: object) -> bool:
        if not type(other) == Self: return False
        other = cast(Self, other)
        return self.segments == other.segments
    
    def matches_segment(self, other: Segment) -> bool:
        return any(_self.matches(other) for _self in self.segments)
    
    def matches_side(self, other: Self) -> bool:
        return any(_self.matches(_other) for _other in other.segments for _self in self.segments)
    
    def merge(self, other: Self):
        self.segments |= other.segments
    
    @classmethod 
    def from_merge_of(cls, a: Self, b: Self):
        return cls(chain(a.segments, b.segments))
    
def test_side():
    ...

class Region(Container, Sized, Iterable, Hashable):
    def __init__(self, label: str, positions: Iterable[tuple[int, int]] | None = None):
        self.label = label
        self._sides: set[Side] = set()

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

    def discard(self, o:tuple[int, int]):
        self.positions.discard(o)

    @property
    def area(self) -> int:
        return len(self)
    
    def side_segments(self) -> Generator[tuple[float, float]]:
        for p in self:
            for n in Map.neighbors_unrestricted(p):
                if n not in self:
                    yield ((p[0]+n[0])/2, (p[1]+n[1])/2,)
    
def test_region():
    ...

def test_map():
    m = Map.from_path("day12/dataE.txt")
    assert len(m.regions) == 3

    ...
  

class Map(UserDict):
    def __init__(self, max_lines:int, max_chars:int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_lines = max_lines
        self.max_chars = max_chars
        self._regions: defaultdict[tuple[int, int], Region] = self.init_regions(self.data)
        
    
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

    
    def init_regions(self, data: dict[tuple[int, int], str]) -> defaultdict[tuple[int, int], Region]:
        to_consider: list[tuple[int, int]] = [(0, 0)]
        first_region = Region(data[(0,0)], [(0, 0)])
        null_region = Region("Null", [])

        regions: defaultdict[tuple[int, int], Region ] = defaultdict(lambda: null_region)
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
    
    def get_regions_from_segment(self, seg: tuple[float, float]) -> tuple[Region, Region]:
        if seg[0] == int(seg[0]): # (1, 2.5)
            assert seg[1] != int(seg[1])
            return (self._regions[(int(seg[0]), int(seg[1]))], self._regions[(int(seg[0]), int(seg[1]+1))])
        elif seg[1] == int(seg[1]): # (1.5, 3)
            assert seg[0] != int(seg[0])
            return (self._regions[(int(seg[0]), int(seg[1]))], self._regions[(int(seg[0])+1, int(seg[1]))])
        else:
            raise ValueError(f"{seg} has no integer parts")

    def num_sides(self, region: Region) -> int:
        assert region in self.regions

        self._sides: set[Side] = set()
        for seg in region.side_segments():
            new_segment = Segment(seg, self.get_regions_from_segment(seg))
            found_match = False
            for side in self._sides:
                if side.matches_segment(new_segment) and not found_match:
                    print(f"Adding segment {new_segment} to side {side}")
                    side.add(new_segment)
                    found_match = True
                    break
            if not found_match:
                print(f"Starting new side with seg {seg}")
                self._sides.add(Side([new_segment]))
        print(f">>>{region.label}: Before dedup there {len(self._sides)=}")
        print("\n".join("\t" + str(s) for s in self._sides))
        
        #deduplicate
        queue: deque[Side] = deque(self._sides)

        
        output = []
        while (queue):
            m = queue.popleft()
            looked_at = 0
            while True and len(queue) > 0:
                item = queue.popleft()
                if m.matches_side(item):
                    m.merge(item)
                    looked_at = 0
                else:
                    queue.append(item)
                    looked_at += 1
                if looked_at >= len(queue): # +1?
                    break
            output.append(m)
        
        self._sides = set(output)
        print(f"{region.label}: After dedup {len(self._sides)=}\n\n")
        print("\n".join("\t" + str(s) for s in sorted(self._sides, key=lambda x: min(s.segment[0] for s in x.segments))))
        return len(self._sides)
    
    def price_in_map(self, region: Region) -> int:
        assert region in self.regions
        return region.area * self.num_sides(region)
    


if __name__ == "__main__":
    myMap = Map.from_path("day12/dataabc.txt")
    #print(myMap)
    #for r in myMap.regions:
    #    print(f"{r} Num_Sides:{r.num_sides} Price:{r.price_in_map(myMap)}")
    print(f"Total cost: {sum(myMap.price_in_map(r) for r in myMap.regions)}")
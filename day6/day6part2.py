from enum import Enum

type Position = tuple[int, int]

class Direction(Enum):
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)
    

def load_data(raw: list[str]) -> tuple[set[Position], Position, int, int]:
    obstacles = set()
    for l, line in enumerate(raw):
        for c, char in enumerate(line):
            if char == "#": obstacles.add((l, c))
            elif char == "^": start = (l, c)

    if start is None: raise ValueError("Start position not found")
    return obstacles, start, len(raw), len(raw[0])

def inbound(l, c, max_line, max_chars):
    return 0 <= l < max_line and 0 <= c < max_chars


if __name__ == '__main__':
    with open('day6/data.txt', 'r') as f:
        obstacles, location, num_lines, num_chars = load_data(f.readlines())
    
    occupied: set[tuple[Position, Direction]] = set()
    direction = Direction.NORTH

    while inbound(*location, num_lines, num_chars):
        occupied.add(location)
        next_location = (location[0] + direction.value[0], location[1] + direction.value[1])
        if next_location in obstacles:
            match direction:
                case Direction.NORTH: # NORTH
                    direction = Direction.EAST # EAST
                case  Direction.EAST:
                    direction = Direction.SOUTH
                case  Direction.SOUTH:
                    direction = Direction.WEST
                case  Direction.WEST:
                    direction = Direction.NORTH
        else:
            location = next_location
    
    print(f"{len(occupied)= }")

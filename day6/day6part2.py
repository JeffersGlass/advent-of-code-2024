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
        obstacles, start_location, num_lines, num_chars = load_data(f.readlines())

    count = 0
    for l in range(num_lines):
        for c in range(num_chars):
            location = start_location
            if (l, c) in obstacles:
                #print(f"{str((l, c)): <10} Already an obstacle here")
                continue
            if location == (l, c):
                #print(f"{str((l, c)): <10} Guard starts here!")
                continue # Can't add a new obstacle here
            current_obstacles = obstacles | {(l, c)}
            ##print(current_obstacles)

            occupied: set[tuple[Position, Direction]] = set()
            direction = Direction.NORTH

            while inbound(*location, num_lines, num_chars):
                if (location, direction) in occupied: #already been here
                    print(f"{str((l, c)): <10} Found a loop! ")
                    count += 1
                    break
                occupied.add((location, direction))
                next_location = (location[0] + direction.value[0], location[1] + direction.value[1])
                if next_location in current_obstacles:
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
            else:
                pass
                #print(f"{str((l, c)): <10} Guard exited, no loop found")
    
    print(f"{count= }")

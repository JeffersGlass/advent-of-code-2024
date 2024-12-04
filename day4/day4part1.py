with open('day4/data.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

num_lines = len(lines)
line_length = len(lines[0])

word = 'XMAS'

directions = [(line, char) for line in range(-1, 2) for char in range(-1, 2) if (line, char) != (0, 0)]

def inbounds(line, char):
    return line >= 0 and line < num_lines and char >= 0 and char < line_length

total = 0
for l, line in enumerate(lines):
    for c, char in enumerate(line):
        print(l, c)
        # starting position
        if char != word[0]: continue #short circuit from X
        for direction in directions:
            valid = True
            #Starting position and direction
            for dir_mult in range(1, 4):
                look_loc = (l+(direction[0]*dir_mult), c + (direction[1]*dir_mult))
                if inbounds(*look_loc) and lines[look_loc[0]][look_loc[1]] == word[dir_mult]:
                    pass
                else:
                    valid = False
                    break
            if valid: 
                total += 1

print(f"{total=}")



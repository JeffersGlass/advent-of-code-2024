with open('day4/data.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

num_lines = len(lines)
line_length = len(lines[0])

direction_sets = (
    ((1, -1), (-1, 1)),
    ((1, 1), (-1, -1))
)

def inbounds(line, char):
    return line >= 0 and line < num_lines and char >= 0 and char < line_length

total = 0
for l, line in enumerate(lines):
    for c, char in enumerate(line):
        # starting position
        if char != 'A': continue #short circuit from X
        valid = True
        for diagonal in direction_sets:
            letters = []
            for dir in diagonal:
                if inbounds(l + dir[0], c + dir[1]):
                    letters.append(lines[l+dir[0]][c+dir[1]])
                else:
                    valid = False
                    break
            if not valid: break
            if not (letters.count('M') == 1 and letters.count('S') == 1):
                valid = False
        if valid:
            total += 1

print(f"{total= }")



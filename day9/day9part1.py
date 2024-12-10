from enum import Enum, auto

class LOAD_STATE(Enum):
    FILE = auto()
    BLANK = auto()

def load_data(raw: str) -> list[int]:
    data: list[int] = []
    block_num: int = 0
    state = LOAD_STATE.FILE

    for char in raw:
        num = int(char)
        if state == LOAD_STATE.FILE:
            data.extend([block_num] * num)
            block_num += 1
            state = LOAD_STATE.BLANK
        else:
           data.extend([-1] * num) # -1 denotes an empty block
           state = LOAD_STATE.FILE
        
    return data

def compactify_data(data: list[int]) -> list[int]:
    p1 = 0
    p2 = len(data) - 1

    while p2 >= p1:
        while data[p1] != -1:
            p1 += 1
        while data[p2] == -1:
            p2 -= 1
        if p2 <= p1: break
        data[p1], data[p2] = data[p2], data[p1]
    return data

def score_data(data: list[int]) -> int:
    return sum(i * val for i, val in enumerate(data) if val >= 0)

def print_data(data: list[int]):
    for num in data:
        if num >= 0:
            if num >= 10:
                print(f"[{num}]", end = "")
            else:
                print(f"{num}", end = "")
        else: print(".", end = "")
    print("")



if __name__ == "__main__":
    with open("day9/data.txt", "r") as f:
        data = load_data(f.read().strip())
    data = compactify_data(data)
    print(f"{score_data(data)= }")

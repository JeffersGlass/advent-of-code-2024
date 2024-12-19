from collections.abc import Container
from enum import Enum, auto
from operator import attrgetter, itemgetter
from typing import cast
from dataclasses import dataclass

@dataclass
class BlockData(Container):
    start_index: int
    length: int

    def __contains__(self, x: object) -> bool:
        if not issubclass(type(x), int):
            raise TypeError("BlockData can only 'contain' ints, not " + str(type(x)))
        x = cast(int, x)
        return self.start_index <= x < self.start_index + self.length

class LOAD_STATE(Enum):
    FILE = auto()
    BLANK = auto()

def load_data(raw: str) -> tuple[dict[int, BlockData], list[BlockData]]:
    data_blocks: dict[int, BlockData] = dict()
    zero_blocks: list[BlockData] = list()
    block_num: int = 0
    start_index: int = 0
    state = LOAD_STATE.FILE

    for char in raw:
        num = int(char)
        if state == LOAD_STATE.FILE:
            data_blocks[block_num] = BlockData(start_index=start_index, length=num)
            block_num += 1
            start_index += num
            state = LOAD_STATE.BLANK
        else:
           zero_blocks.append(BlockData(start_index=start_index, length=num))
           start_index += num
           state = LOAD_STATE.FILE
        
    return data_blocks, zero_blocks

def compactify_files(data_blocks: dict[int, BlockData], zero_blocks: list[BlockData]) ->  dict[int, BlockData]:
    max_id = max(k for k in data_blocks.keys())

    for file_id in range(max_id, 0, -1):
        #print(f"Examining file id {file_id}")
        valid_holes = sorted([hole for hole in zero_blocks if hole.length >= data_blocks[file_id].length and hole.start_index < data_blocks[file_id].start_index], key=attrgetter('start_index'))
        if valid_holes: # insert data block in smaller hole
            #print(f"Trying to move file {data_blocks[file_id]} to hole at {valid_holes[0].start_index}")
            old_block_start = data_blocks[file_id].start_index
            old_block_length = data_blocks[file_id].length
            data_blocks[file_id] = BlockData(start_index=valid_holes[0].start_index, length = data_blocks[file_id].length)
            #print(f"New block is {data_blocks[file_id]}")
            new_length = data_blocks[file_id].length - valid_holes[0].length
            zero_blocks.remove(valid_holes[0])
            if new_length:
                zero_blocks.append(BlockData(length=valid_holes[0].length - data_blocks[file_id].length, start_index=valid_holes[0].start_index + data_blocks[file_id].length))

        else: 
            ...

    return data_blocks


def score_data(data_blocks:  dict[int, BlockData]) -> int:
    total =0
    for i, block in data_blocks.items():
        for j in range(block.start_index, block.start_index + block.length):
            total += i * j
    return total
    
    #return sum(i * val for i, val in enumerate(data) if val >= 0)

def output_data(data: dict[int, BlockData]) -> str:
    blocks = sorted(data.items(), key= lambda x : x[1].start_index)
    p1 = 0
    result = []
    
    while(blocks):
        if p1 in blocks[0][1]:
            result.append(str(blocks[0][0]))
        else:
            result.append(".")

        if p1 >= (blocks[0][1].start_index + blocks[0][1].length) - 1:
            blocks = blocks[1:]
            if not blocks: break

        p1 += 1
    
    return "".join(result)

if __name__ == "__main__":
    with open("day9/data.txt", "r") as f:
        data, zeros = load_data(f.read().strip())
    #print(output_data(data))
    data = compactify_files(data, zeros)
    #print(output_data(data))
    print(f"{score_data(data)= }")

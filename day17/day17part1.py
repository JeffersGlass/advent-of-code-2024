from computer import Computer

import logging
import re

if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG)
    with open("day17/data.txt", "r") as f:
        data = f.read()

    a = re.search(r"Register A: (\d+)", data)
    b = re.search(r"Register B: (\d+)", data)
    c = re.search(r"Register C: (\d+)", data)
    prog = re.search(r"Program: ([\d,]+)", data)

    #a = 1
    a = 1
    while True:
        comp = Computer(
            [int(s) for s in prog.group(1).split(",")],
            (a,
            int(b.group(1)),
            int(c.group(1))),
        )
        print(comp.readable())
        #print(comp)
        comp.run()
        input(f"{a=} {comp.output= } ?= Program: '{",".join(str(s) for s in comp.instr)}'")
        if comp.output == ",".join(str(s) for s in comp.instr):
            print(f"Smallest A: {a}")
            exit()
        a += 1
        

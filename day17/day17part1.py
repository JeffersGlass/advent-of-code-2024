from computer import Computer

import logging
import re

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    with open("day17/data.txt", "r") as f:
        data = f.read()

    a = re.search(r"Register A: (\d+)", data)
    b = re.search(r"Register B: (\d+)", data)
    c = re.search(r"Register C: (\d+)", data)
    prog = re.search(r"Program: ([\d,]+)", data)

    c = Computer((int(s) for s in prog.group(1).split(",")), (int(a.group(1)), int(b.group(1)), int(c.group(1))))
    print(str(c))
    c.run()
    print(c.output)
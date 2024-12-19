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

    a = 1
    #a = 2 ** (3*15)
    output_jumps: list[int] = []
    first_matches: list[int] = []
    try:
        while True:
            print("\n\n")
            comp = Computer(
                [int(s) for s in prog.group(1).split(",")],
                (a,
                int(b.group(1)),
                int(c.group(1))),
            )
            print(comp.readable())
            while False: ###
                if comp.ip > len(comp.instr) - 1: break
                print(comp)
                input(comp.inst_to_str(comp.ip))
                if not comp.do_instruction(): break
                
            #print(comp)


            comp.run()
            #if len(comp._output) > len(output_jumps): output_jumps.append(a); print(f"{output_jumps= }")
            #if len(comp._output) > len(first_matches) and comp._output == comp.instr[-(len(first_matches) + 1):]: 
            #    first_matches.append(a); 
            #    print(f"{first_matches= }")
            #    print(f"{print("\n".join("{0:o}".format(match) for match in first_matches))}")
            #    print(f"{comp._output=}")

            input(f"{a=: <6} {comp.output= } ?= Program: '{",".join(str(s) for s in comp.instr)}'")
            if comp.output == ",".join(str(s) for s in comp.instr):
                print(f"Smallest A: {a}")
                exit()
            a += 1
            if not a % 1000:
                print(a)
            
    except KeyboardInterrupt as err:
        print(f"\n\n{output_jumps= }\n")
        print(f"{first_matches= }")
        print(f"{print("\n".join("{0:o}".format(match) for match in first_matches))}")
        raise (err)
        

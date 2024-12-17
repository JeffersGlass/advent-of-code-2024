import logging
import re
from typing import TypedDict, Iterable

class Registers(TypedDict):
    a: int
    b: int
    c: int

class Computer:
    def __init__(self, instr: Iterable[int], r: tuple[int, int, int] | None = None):
        self.instr = list(instr)

        self.registers: Registers 
        if r: self.registers = {"a": r[0], "b": r[1], "c":r[2]}
        else: self.registers = {"a": 0, "b": 0, "c": 0}

        self.ip: int = 0
        self._output: list[str] = list()

    def __repr__(self) -> str:
        return f"Register(instr={self.instr}, ip={self.ip}, registers={self.registers}, output={self.output})"

    @property
    def output(self):
        return ",".join(s for s in self._output)

    def do_instruction(self) -> bool:
        if self.ip > len(self.instr) - 1: return False
        else:
            ins = self.instr[self.ip]
            operand = self.instr[self.ip+1]

        self.handle_op(ins, operand)
        return True

    def handle_op(self, i: int, operand: int):
        logging.debug(f"Inst {i: <2} {operand: <20}")
        match i:
            case 0: #adv
                self.registers['a'] = int(self.registers['a'] / (2 ** self.combo_operand(operand)))
                self.ip += 2
            case 1: #bxl
                self.registers["b"] = self.registers["b"] ^ operand
                self.ip += 2
            case 2: #bst
                self.registers["b"] = self.combo_operand(operand) % 8
                self.ip += 2
            case 3: #jnz
                if self.registers["a"] != 0:
                    self.ip = operand
                else:
                    self.ip += 2
            case 4: #bxc
                self.registers['b'] = self.registers['b'] ^ self.registers['c']
                self.ip += 2
            case 5: #out
                self._output.append(str(self.combo_operand(operand) % 8))
                self.ip += 2
            case 6: #bdv
                self.registers['b'] = int(self.registers['a'] / 2 ** self.combo_operand(operand))
                self.ip += 2
            case 7: #cdv
                self.registers['c'] = int(self.registers['a'] / 2 ** self.combo_operand(operand))
                self.ip += 2


    def combo_operand(self, operand: int) -> int:
        if 0 <= operand <= 3: return operand
        if operand == 4: return self.registers['a']
        if operand == 5: return self.registers['b']
        if operand == 6: return self.registers['c']
        raise ValueError(f"{operand} is not a valid combo operand")
    
    def halt(self):
        return ",".join(s for s in self._output)

    def run(self):
        while self.do_instruction():
            ...
        self.halt()

def test_ops():
    c = Computer((2, 6), (0, 0, 9))
    c.do_instruction()
    assert c.registers['b'] == 1

    c = Computer((5,0,5,1,5,4), (10, 0, 0))
    c.run()
    assert c.output == "0,1,2"

    c = Computer((0,1,5,4,3,0), (2024, 0, 0))
    c.run()
    assert c.output == "4,2,5,6,7,7,7,7,3,1,0"
    assert c.registers['a'] == 0

    c = Computer((1,7), (0, 29, 0))
    c.run()
    assert c.registers['b'] == 26

    c = Computer((4,0), (0, 2024, 43690))
    c.run()
    assert c.registers['b'] == 44354
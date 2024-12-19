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
        if r:
            self.registers = {"a": r[0], "b": r[1], "c": r[2]}
        else:
            self.registers = {"a": 0, "b": 0, "c": 0}

        self.ip: int = 0
        self._output: list[int] = list()

    def __repr__(self) -> str:
        return f"Computer(instr={self.instr}, ip={self.ip}, registers={self.registers}, output={self.output})"
    
    readable_format = "{line: <3}{short: <5}{raw_op: <3}{combo_op: <12}{long: <80}"

    @property
    def output(self):
        return ",".join(str(s) for s in self._output)

    def do_instruction(self) -> bool:
        if self.ip > len(self.instr) - 1:
            return False
        else:
            ins = self.instr[self.ip]
            operand = self.instr[self.ip + 1]

        self.handle_op(ins, operand)
        return True
    
    def readable(self) -> str:
        result = []
        result.append(self.readable_format.format(line="##", short="Name", raw_op="Op", combo_op="ComboOp?", long="Long Description"))
        for ip in range(0, len(self.instr), 2):
            result.append(self.inst_to_str(ip))
        
        return "\n".join(result)
            

            

    def inst_to_str(self, ip) -> str:
        inst, op = self.instr[ip], self.instr[ip+1]
        match inst:
            case 0:
                name, combo, long = "adv", str(self.combo_operand(op)), f"Divide A register by 2 ** {str(self.combo_operand(op))} -> A"
            case 1:
                name, combo, long = "bxl", "", f"B ^ {op} -> B"
            case 2:
                name, combo, long = "bst", str(self.combo_operand(op)), f"{str(self.combo_operand(op))} % 8 -> B"
            case 3:
                name, combo, long = "jnz", "", f"Jump to {op} if A != 0"
            case 4:
                name, combo, long = "bxc", "", "B ^ C -> B"
            case 5:
                name, combo, long = "out", f"{str(self.name_combo_operand(op))}", f"Output {str(self.name_combo_operand(op))} % 8"
            case 6:
                name, combo, long = "bdv", str(self.name_combo_operand(op)), f"Divide A register by 2 ** {str(self.name_combo_operand(op))} -> B"
            case 7:
                name, combo, long = "cdv", str(self.name_combo_operand(op)),f"Divide A register by 2 ** {str(self.name_combo_operand(op))} -> C"
        
        return (self.readable_format.format(line=ip, short=name, raw_op=op, combo_op=combo, long=long))



    def handle_op(self, i: int, operand: int):
        logging.debug(f"Inst {i: <2} {operand: <20}")
        match i:
            case 0:  # adv
                self.registers["a"] = int(
                    self.registers["a"] / (2 ** self.combo_operand(operand))
                )
                self.ip += 2
            case 1:  # bxl
                self.registers["b"] = self.registers["b"] ^ operand
                self.ip += 2
            case 2:  # bst
                self.registers["b"] = self.combo_operand(operand) % 8
                self.ip += 2
            case 3:  # jnz
                if self.registers["a"] != 0:
                    self.ip = operand
                else:
                    self.ip += 2
            case 4:  # bxc
                self.registers["b"] = self.registers["b"] ^ self.registers["c"]
                self.ip += 2
            case 5:  # out
                self._output.append(self.combo_operand(operand) % 8)
                self.ip += 2
            case 6:  # bdv
                self.registers["b"] = int(
                    self.registers["a"] / 2 ** self.combo_operand(operand)
                )
                self.ip += 2
            case 7:  # cdv
                self.registers["c"] = int(
                    self.registers["a"] / 2 ** self.combo_operand(operand)
                )
                self.ip += 2

    def combo_operand(self, operand: int) -> int:
        if 0 <= operand <= 3:
            return operand
        if operand == 4:
            return self.registers["a"]
        if operand == 5:
            return self.registers["b"]
        if operand == 6:
            return self.registers["c"]
        raise ValueError(f"{operand} is not a valid combo operand")
    
    def name_combo_operand(self, operand: int) -> str:
        if 0 <= operand <= 3:
            return f"Literal {operand}"
        if operand == 4:
            return "[A Value]"
        if operand == 5:
            return "[B Value]"
        if operand == 6:
            return "[C Value]"
        raise ValueError(f"{operand} is not a valid combo operand")

    def run(self):
        while self.do_instruction():
            ...


def test_ops():
    c = Computer((2, 6), (0, 0, 9))
    c.do_instruction()
    assert c.registers["b"] == 1

    c = Computer((5, 0, 5, 1, 5, 4), (10, 0, 0))
    c.run()
    assert c.output == "0,1,2"

    c = Computer((0, 1, 5, 4, 3, 0), (2024, 0, 0))
    c.run()
    assert c.output == "4,2,5,6,7,7,7,7,3,1,0"
    assert c.registers["a"] == 0

    c = Computer((1, 7), (0, 29, 0))
    c.run()
    assert c.registers["b"] == 26

    c = Computer((4, 0), (0, 2024, 43690))
    c.run()
    assert c.registers["b"] == 44354

def test_comp():
    instr = (0,3,5,4,3,0)
    c = Computer(instr, (117440, 0, 0))
    c.run()
    print(c.output)
    assert c.output == ','.join(str(s) for s in instr)
import itertools
from colored import Fore, Back, Style

type equation_parts = tuple[int, list[int]]

def load_data(raw: list[str]) -> equation_parts:
    eq_data = list()
    for line in raw:
        result, rest = line.split(':')
        nums = [int(r.strip()) for r in rest.split()]
        eq_data.append((int(result), nums))
    return eq_data

def new_op(x: int, new: tuple[str, int]) -> int:
    op, next_num = new
    match op:
        case "+":
            return x + next_num
        case "*":
            return x * next_num
        case "_":
            return int(str(x) + str(next_num))

if __name__ == "__main__":
    with open('day7/data.txt', 'r') as f:
        data = load_data(f.readlines())
        
    possible = 0
    for eq in data:
        result, nums = eq
        for ops in itertools.product("+*_", repeat=len(nums) - 1):
            eval_string_iter = itertools.accumulate(zip(ops, nums[1:]), func=new_op, initial = nums[0])
            for n in eval_string_iter:
                calculated = n
            correct = (calculated == result)
            if correct:
                print(f"{Fore.green if correct else Fore.white}", str(nums[0]) + "".join(f"{s[0]}{s[1]}" for s in zip(ops, nums[1:])), "=", calculated, f"{'==' if correct else '!='}", result)
                possible += result
                break

    print(f"{possible= }")
    print(f"{Style.reset}")
import itertools
from colored import Fore, Back, Style

type equation_parts = tuple[int, list[int]]

def load_data(raw: list[str]) -> equation_parts:
    eq_data = list()
    for line in raw:
        result, rest = line.split(':')
        nums = [r.strip() for r in rest.split()]
        eq_data.append((int(result), nums))
    return eq_data

new_op = lambda x, new: f"({x}{new[0]}{new[1]})"

if __name__ == "__main__":
    with open('day7/data.txt', 'r') as f:
        data = load_data(f.readlines())
        
    possible = 0
    for eq in data:
        result, nums = eq
        for ops in itertools.product("+*", repeat=len(nums) - 1):
            calc_string_iter = itertools.accumulate(zip(ops, nums[1:]), func=new_op, initial = nums[0])
            for n in calc_string_iter:
                calc_string = n
            calc = eval(calc_string)
            correct = (calc == result)
            if correct:
                print(f"{Fore.green if correct else Fore.white}",calc_string, "=", calc, f"{'=' if correct else '!='}", result)
            if calc == result:
                possible += result
                break

    print(f"{possible= }")
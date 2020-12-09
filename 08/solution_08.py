def load_bootcode(filepath) -> list[tuple[str, int]]:
    instructions = []
    with open(filepath, 'r') as infile:
        for line in infile.readlines():
            code, num = line.strip().split()
            instructions.append((code, int(num)))
    return instructions


def run_code(instructions, pos=0, acc=0, seen_codes=None) -> tuple[bool, int]:
    """ Returns tuple (success, acc) """
    if pos >= len(instructions):
        return True, acc

    if seen_codes and pos in seen_codes:
        return False, acc
    else:
        if not seen_codes:
            seen_codes = set()
        seen_codes.add(pos)

    code, num = instructions[pos]
    if code == 'jmp':
        return run_code(instructions, pos + num, acc, seen_codes)
    elif code == 'acc':
        acc += num

    return run_code(instructions, pos + 1, acc, seen_codes)


def fix_code(instructions):
    """ Bruteforce switching each nop/jmp and run code each time """
    for pos, (code, num) in enumerate(instructions):
        if code == 'nop':
            new_instructions = instructions.copy()
            new_instructions[pos] = ('jmp', num)
        elif code == 'jmp':
            new_instructions = instructions.copy()
            new_instructions[pos] = ('nop', num)
        else:
            continue

        success, acc = run_code(new_instructions)

        if success:
            return acc


boot_code = load_bootcode('input.txt')
# Part 1
print(run_code(boot_code))
# Part 2
print(fix_code(boot_code))

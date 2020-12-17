from collections import defaultdict
from itertools import product


def parse_mask(mask: str):
    ones, zeroes, floaters = set(), set(), set()

    for i, v in enumerate(reversed(list(mask))):
        if v == '1':
            ones.add(i)
        elif v == '0':
            zeroes.add(i)
        else:
            floaters.add(i)

    return ones, zeroes, floaters


def load_program(filepath):
    ones, zeroes = set(), set()

    with open(filepath, 'r') as infile:
        for line in infile.readlines():
            if line.startswith('mask'):
                ones, zeroes, floaters = parse_mask(line.split()[-1].strip())
                continue

            addr, value = line.strip().lstrip('mem[').split('] = ')

            yield ones, zeroes, floaters, int(addr), int(value)


def write_values_to_memory(filepath):
    register = defaultdict(int)
    for ones, zeroes, _, addr, value in load_program(filepath):

        for i in ones:
            value |= 1 << i
        for i in zeroes:
            value &= ~(1 << i)

        register[addr] = value
    return sum(register.values())


def decode_memory_addresses(filepath):
    register = defaultdict(int)
    for ones, _, floaters, addr, value in load_program(filepath):
        addresses = set()

        for i in ones:
            addr |= 1 << i

        for comb in product({0, 1}, repeat=len(floaters)):
            new_addr = addr
            for i, c in zip(floaters, comb):
                if c == 1:
                    new_addr |= 1 << i
                if c == 0:
                    new_addr &= ~(1 << i)
            addresses.add(new_addr)

        for ad in addresses:
            register[ad] = value

    return sum(register.values())


# Part 1
print(write_values_to_memory('input.txt'))
# Part 2
print(decode_memory_addresses('input.txt'))

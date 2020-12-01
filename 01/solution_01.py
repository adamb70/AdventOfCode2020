from functools import reduce
from operator import mul
from itertools import combinations


def find_sum(numbers, target, comb_length):
    for comb in combinations(numbers, comb_length):
        if sum(comb) == target:
            return reduce(mul, comb)


with open('input.txt', 'r') as infile:
    numbers = [int(x.strip()) for x in infile.readlines()]

# Part 1
print(find_sum(numbers, 2020, 2))
# Part 2
print(find_sum(numbers, 2020, 3))

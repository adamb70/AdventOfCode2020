from itertools import combinations


def load_numbers(filepath) -> list[int]:
    with open(filepath, 'r') as infile:
        return [int(x) for x in infile.read().splitlines()]


def validate_numbers(numbers, preamble_len: int):
    for i in range(preamble_len, len(nums)):
        num = nums[i]
        for comb in combinations(numbers[i - preamble_len:i], 2):
            if sum(comb) == num:
                break
        else:
            return num


def find_contiguous_set(numbers, target):
    """ Bruteforces contiguous subsets of the list until the sum == target """
    for r in range(2, len(numbers)):
        for n in range(len(numbers) - r + 1):
            num_set = numbers[n:n + r]
            if sum(num_set) == target:
                return min(num_set) + max(num_set)


nums = load_numbers('input.txt')

# Part 1
invalid_num = validate_numbers(nums, 25)
print(invalid_num)
# Part 2
print(find_contiguous_set(nums, invalid_num))

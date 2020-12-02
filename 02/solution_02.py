from collections import Counter


def is_valid_part_1(min_max, letter, password):
    count = Counter(password)
    return min_max[0] <= count[letter] <= min_max[1]


def is_valid_part_2(indexes, letter, password):
    first_match = password[indexes[0] - 1] == letter
    second_match = password[indexes[1] - 1] == letter
    return first_match != second_match


valid_1 = 0
valid_2 = 0

with open('input.txt', 'r') as infile:
    for line in infile.readlines():
        min_max, letter, password = line.split()
        min_max = tuple(int(x) for x in min_max.split('-'))
        letter = letter[:-1]

        valid_1 += is_valid_part_1(min_max, letter, password)
        valid_2 += is_valid_part_2(min_max, letter, password)

# Part 1
print(valid_1)
# Part 2
print(valid_2)

from collections import Counter, defaultdict


def load_adaptors(filepath) -> list[int]:
    with open(filepath, 'r') as infile:
        return sorted([int(x) for x in infile.read().splitlines()])


def count_differences(adaptors):
    differences = []
    for i, num in enumerate(adaptors):
        if i == 0:
            differences.append(num)
            continue

        differences.append(num - adaptors[i - 1])

        if i == len(adaptors) - 1:
            differences.append(3)

    count = Counter(differences)
    return count[1] * count[3]


def distinct_arrangements(adaptors):
    # Add starting and ending points to adaptor list
    adaptors = [0] + adaptors
    adaptors.append(adaptors[-1] + 3)

    arrangement = defaultdict(int)
    # First adapter counts as one path
    arrangement[0] = 1

    for n in adaptors[1:]:
        # Numbers of paths to each step is equal to sum of previous three steps
        arrangement[n] = arrangement[n - 1] + arrangement[n - 2] + arrangement[n - 3]

    return arrangement[max(arrangement.keys())]



adaptor_list = load_adaptors('input.txt')
# Part 1
print(count_differences(adaptor_list))
# Part 2
print(distinct_arrangements(adaptor_list))

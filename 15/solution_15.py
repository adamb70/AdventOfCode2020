from collections import defaultdict


def get_last_spoken_number(turns):
    with open('input.txt', 'r') as infile:
        starting_numbers = [int(n) for n in infile.read().strip().split(',')]

    # Set initial values
    spoken_nums = set(starting_numbers[:-1])
    turn_spoken = defaultdict(lambda: -1)
    for i, s in enumerate(starting_numbers[:-1]):
        turn_spoken[s] = i

    num = starting_numbers[-1]

    for turn in range(len(starting_numbers), turns):
        last_spoken = turn_spoken[num]
        if last_spoken == -1:
            spoken_nums.add(num)
            new_num = 0
        else:
            new_num = turn - last_spoken - 1

        turn_spoken[num] = turn - 1

        num = new_num

    return num


# Part 1
print(get_last_spoken_number(2020))
# Part 2
print(get_last_spoken_number(30000000))

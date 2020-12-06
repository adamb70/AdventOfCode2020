def load_groups(filepath):
    groups = []
    with open(filepath, 'r') as infile:
        answers = infile.read().splitlines()
        answers.append('')  # Add empty line to bottom of file to make splitting groups easier

        people = []
        for p in answers:
            if p == '':
                groups.append(people)
                people = []
                continue
            people.append(p)

    return groups


def count_any_yes_in_group(groups):
    total = 0
    for g in groups:
        total += len(set(question for person in g for question in person))

    return total


def count_all_yes_in_group(groups):
    total = 0
    for g in groups:
        # Makes a set of every person's answer, and calculates the intersection for all
        total += len(set.intersection(*(set(person) for person in g)))

    return total


groups_list = load_groups('input.txt')
# Part 1
print(count_any_yes_in_group(groups_list))
# Part 2
print(count_all_yes_in_group(groups_list))

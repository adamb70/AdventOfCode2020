import re


def load_rules(filepath) -> dict[str, dict[str, int]]:
    pattern = re.compile(r'^(\d+) ([\w\s]+?) bags?')
    with open(filepath, 'r') as infile:
        rules = {}
        for rule in infile.readlines():
            outer, inner = rule.split(' bags contain ')
            inner = inner.strip().split(', ')

            if len(inner) == 1 and inner[0] == 'no other bags.':
                rules[outer] = None
            else:
                bags = {}
                for bag in inner:
                    match = re.search(pattern, bag)
                    bags[match.group(2)] = int(match.group(1))
                rules[outer] = bags

    return rules


def find_bags_containing(target: str, bag_rules: dict[str, dict[str, int]]) -> set:
    bad_bags = set(bag_rules[target].keys())  # Don't need to check bags inside the target
    good_bags = set()

    def check_inner(bag):
        inner_bags = bag_rules[bag]

        if not inner_bags:
            bad_bags.add(bag)
            return False

        if bag in good_bags:
            return True

        if bag in bad_bags or bag == target:
            return False

        if target in inner_bags.keys():
            good_bags.add(bag)
            return True

        for inner in inner_bags:
            if check_inner(inner):
                good_bags.add(bag)
                return True

    for outer_bag in bag_rules:
        check_inner(outer_bag)

    return good_bags


def count_total_bags_inside(target: str, bag_rules: dict[str, dict[str, int]]) -> int:
    counts = {}

    def count_inside(bag: str) -> int:
        if c := counts.get(bag):
            # Check existing counts
            return c

        inner_bags = bag_rules[bag]

        if not inner_bags:
            counts[bag] = 0
            return 0

        count = 0
        for inner, num in inner_bags.items():
            inner_count = count_inside(inner)
            count += num * (inner_count + 1)  # Add 1 because we are counting the bag as well as the inner bags

        counts[bag] = count
        return count

    return count_inside(target)



rules_list = load_rules('input.txt')
# Part 1
print(len(find_bags_containing('shiny gold', rules_list)))
# Part 2
print(count_total_bags_inside('shiny gold', rules_list))

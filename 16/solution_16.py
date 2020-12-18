from collections import defaultdict
from itertools import groupby


def load_input(input_file):
    with open(input_file, 'r') as infile:
        input_rules, input_ticket, input_nearby = [list(y) for x, y in
                                                   groupby(infile.read().splitlines(), lambda z: z == '') if not x]
        rules = {}
        for r in input_rules:
            key, vals = r.split(': ')
            l_range, r_range = vals.split(' or ')
            l_min, l_max = l_range.split('-')
            r_min, r_max = r_range.split('-')
            rules[key] = ((int(l_min), int(l_max)), (int(r_min), int(r_max)))

        ticket_numbers = [int(x) for x in input_ticket[1].split(',')]

        nearby_tickets = []
        for line in input_nearby[1:]:
            nearby_tickets.append([int(x) for x in line.split(',')])

    return rules, ticket_numbers, nearby_tickets


def check_rule(num, l_rule, r_rule):
    if l_rule[0] <= num <= l_rule[1] or r_rule[0] <= num <= r_rule[1]:
        return True
    return False


def calculate_error_rate(rules, tickets):
    invalid_nums = []

    for ticket_nums in tickets:
        for num in ticket_nums:
            if not any(check_rule(num, l_rule, r_rule) for l_rule, r_rule in rules.values()):
                invalid_nums.append(num)

    return sum(invalid_nums)


def get_valid_tickets(rules, tickets):
    valid_tickets = []

    for ticket_nums in tickets:
        for num in ticket_nums:
            if not any(check_rule(num, l_rule, r_rule) for l_rule, r_rule in rules.values()):
                break
        else:
            valid_tickets.append(ticket_nums)

    return valid_tickets


def calculate_departure_total(valid_tickets, my_ticket_numbers):
    ticket_length = len(valid_tickets[0])
    valid_pos_rules = defaultdict(list)

    # Find all possible valid positions for each rule
    for pos in range(ticket_length):
        for k, v in rules.items():
            l_rule, r_rule = v
            if all(check_rule(nums[pos], l_rule, r_rule) for nums in valid_tickets):
                valid_pos_rules[pos].append(k)

    completed = set()

    # Narrow down valid position rules until all positions have only one rule
    while max([len(x) for x in valid_pos_rules.values()]) > 1:
        for k, possible_rules in valid_pos_rules.items():
            # Find a pos with a single rule, and remove this rule at every other pos
            if len(possible_rules) == 1 and k not in completed:
                completed.add(k)
                selected_rule = possible_rules[0]  # Get first (only) item in the set

                # Go back over every rule and remove selected_rule
                for k2 in valid_pos_rules.keys():
                    if k2 != k:
                        try:  # Try to remove rule, or fail silently
                            valid_pos_rules[k2].remove(selected_rule)
                        except ValueError:
                            continue

    # Sum together ticked numbers if rule starts `departure`
    ret = 1
    for pos, rule in valid_pos_rules.items():
        rule = rule[0]
        if rule.startswith('departure'):
            ret *= my_ticket_numbers[pos]

    return ret


rules, my_ticket_numbers, nearby_tickets = load_input('input.txt')

# Part 1
print(calculate_error_rate(rules, nearby_tickets))

# Part 2
valid_tickets = get_valid_tickets(rules, nearby_tickets)
print(calculate_departure_total(valid_tickets, my_ticket_numbers))

import regex
from functools import lru_cache


def load_rules(inputfile):
    rules = {}
    messages = []
    with open(inputfile, 'r') as infile:
        input_rules, input_messages = infile.read().split('\n\n')

        for rule in input_rules.splitlines():
            k, v = rule.split(': ')
            rules[k] = v.replace('"', '')

        for message in input_messages.splitlines():
            messages.append(message)

    return rules, messages


def count_matches(rules, messages, match='0'):
    @lru_cache
    def compile_rule(rule):
        if not rule.isdigit():
            return rule
        else:
            return f'(?:{"".join(compile_rule(x) for x in rules[rule].split())})'

    count = 0
    pattern = regex.compile(compile_rule(match))
    for message in messages:
        if pattern.fullmatch(message):
            count += 1
    return count


rules, messages = load_rules('input.txt')

# Part 1
print(count_matches(rules, messages, match='0'))

# Part 2
rules['8'] = '42 +'
rules['11'] = '(?<R> 42 (?&R)? 31 )'
print(count_matches(rules, messages, match='0'))

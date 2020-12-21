def calculate(chunk):
    operations = []
    nums = []

    for char in chunk.split():
        if char in {'+', '*'}:
            operations.append(char)
        else:
            nums.append(char)

    left = int(nums[0])
    for i in range(1, len(nums)):
        operator = operations[i - 1]
        if operator == '+':
            left = int(left) + int(nums[i])
        elif operator == '*':
            left = int(left) * int(nums[i])
    return left


def parse_parens(line):
    stack = []
    for i, char in enumerate(line):
        if char == '(':
            stack.append(i)
        elif char == ')':
            start = stack.pop(-1)
            chunk = line[start + 1: i]
            line = line[:start] + str(calculate(chunk)).center(len(chunk) + 2) + line[i + 1:]
    return line


def add_parens(line):
    # Strip out all the spaces. This works because all ints in the input are only 1 character
    line = line.replace(' ', '')
    i = 0
    while i < len(line):
        char = line[i]
        if char == '+':
            # search backwards for parens
            stack = []
            for j, c in enumerate(reversed(line[:i])):
                if c == ')':
                    stack.append(j)
                elif c == '(':
                    stack.pop(-1)
                if not stack:
                    line = line[:i - j - 1] + '(' + line[i - j - 1:]
                    i += 1
                    break

            # search forwards for parens
            stack = []
            for j, c in enumerate(line[i + 1:]):
                if c == '(':
                    stack.append(j)
                elif c == ')':
                    stack.pop(-1)
                if not stack:
                    line = line[:j + i + 2] + ')' + line[j + i + 2:]
                    i += 1
                    break
        i += 1
    # Add spaces back in
    return line.replace('+', ' + ').replace('*', ' * ')


def calculate_homework(inputfile, advanced=False):
    with open(inputfile, 'r') as infile:
        total = 0
        for line in infile.read().splitlines():
            if advanced:
                line = add_parens(line)

            line = parse_parens(line)
            total += calculate(line)
        return total


# Part 1
print(calculate_homework('input.txt'))
# Part 2
print(calculate_homework('input.txt', advanced=True))

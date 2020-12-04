import re


class Person:
    required_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
    color_regex = re.compile(r'^#[0-9a-f]{6}$')
    pid_regex = re.compile(r'^[0-9]{9}$')
    eye_colors = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}

    def __init__(self):
        self.fields = dict()

    def contains_required_fields(self):
        return all(field in self.fields for field in self.required_fields)

    def all_fields_valid(self):
        if not self.contains_required_fields():
            return False

        # Call all functions starting with `is_valid_` and return if all valid
        return all(
            getattr(self, validator)() for validator in (
                func for func in dir(self) if func.startswith('is_valid_')
            )
        )

    def is_valid_birth_year(self):
        value = self.fields['byr']
        return 1920 <= int(value) <= 2002

    def is_valid_issue_year(self):
        value = self.fields['iyr']
        return 2010 <= int(value) <= 2020

    def is_valid_expiration_year(self):
        value = self.fields['eyr']
        return 2020 <= int(value) <= 2030

    def is_valid_height(self):
        value = self.fields['hgt']
        if value[-2:] == 'cm':
            return 150 <= int(value[:-2]) <= 193
        elif value[-2:] == 'in':
            return 59 <= int(value[:-2]) <= 76
        return False

    def is_valid_hair_color(self):
        value = self.fields['hcl']
        return re.match(self.color_regex, value)

    def is_valid_eye_color(self):
        value = self.fields['ecl']
        return value in self.eye_colors

    def is_valid_passport_id(self):
        value = self.fields['pid']
        return re.match(self.pid_regex, value)


def load_people(filepath):
    people_list = []
    with open(filepath, 'r') as infile:
        person = Person()
        for line in infile.read().splitlines():
            if line == '':
                people_list.append(person)
                person = Person()
            else:
                for field in line.split():
                    person.fields[field[:3]] = field[4:]

        people_list.append(person)
    return people_list


def count_required_fields(people_list):
    valid_count = 0

    for person in people_list:
        if person.contains_required_fields():
            valid_count += 1

    return valid_count


def count_valid_people(people_list):
    valid_count = 0

    for person in people_list:
        if person.all_fields_valid():
            valid_count += 1

    return valid_count


people = load_people('input.txt')

# Part 1
print(count_required_fields(people))
# Part 2
print(count_valid_people(people))

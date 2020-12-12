from copy import deepcopy


def load_seat_grid(filepath):
    grid = []
    with open(filepath, 'r') as infile:
        for col in infile.read().splitlines():
            grid.append(list(col))
    return Grid(grid)


class Grid:
    directions = {
        (-1, 0,),  # Left
        (1, 0),  # Right
        (0, -1),  # Up
        (0, 1),  # Down
        (-1, -1),  # Left Up
        (-1, 1,),  # Left Down
        (1, -1),  # Right Up
        (1, 1),  # Right Down
    }

    def __init__(self, seats):
        self.seats = seats
        self.height = len(seats)
        self.width = len(seats[0])

    def get_adjacent_seats(self, x, y):
        adjacent = []

        for i, j in self.directions:
            new_x, new_y = x + i, y + j
            if not (0 <= new_x <= self.width - 1 and 0 <= new_y <= self.height - 1):
                continue

            adjacent.append(self.seats[new_y][new_x])

        return adjacent

    def get_visible_seats(self, x, y):
        visible_count = 0

        for i, j in self.directions:
            mult = 1
            while True:
                new_x, new_y = x + i * mult, y + j * mult
                if not (0 <= new_x <= self.width - 1 and 0 <= new_y <= self.height - 1):
                    break
                mult += 1

                if self.seats[new_y][new_x] == 'L':
                    break
                if self.seats[new_y][new_x] == '#':
                    visible_count += 1
                    break

        return visible_count

    def run_step(self, use_adjacent=True):
        new_seats = deepcopy(self.seats)

        for y in range(self.height):
            for x in range(self.width):
                current_seat = self.seats[y][x]

                if use_adjacent:
                    # Use adjacent seats as in part 1
                    adjacent = self.get_adjacent_seats(x, y)
                    if current_seat == 'L' and '#' not in adjacent:
                        new_seats[y][x] = '#'
                    elif current_seat == '#' and adjacent.count('#') >= 4:
                        new_seats[y][x] = 'L'
                else:
                    # Use adjacent seats as in part 2
                    visible = self.get_visible_seats(x, y)
                    if current_seat == 'L' and visible == 0:
                        new_seats[y][x] = '#'
                    elif current_seat == '#' and visible >= 5:
                        new_seats[y][x] = 'L'

        self.seats = new_seats

    def count_final_seats(self, use_adjacent=True):
        last_seats = None
        while last_seats != self.seats:
            last_seats = deepcopy(self.seats)
            self.run_step(use_adjacent)

        return len([x for y in self.seats for x in y if x == '#'])


# Part 1
seat_grid = load_seat_grid('input.txt')
print(seat_grid.count_final_seats())

# Part 2
seat_grid = load_seat_grid('input.txt')
print(seat_grid.count_final_seats(use_adjacent=False))

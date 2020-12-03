import math


class Map:
    def __init__(self, map_file):
        with open(map_file, 'r') as infile:
            self.grid = [[x for x in y.strip()] for y in infile.readlines()]

        self.height = len(self.grid)
        self.width = len(self.grid[0])


class Vec2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vec2({self.x}, {self.y})"


def count_trees_slope(slope_map: Map, slope: Vec2) -> int:
    """ Count number of trees on path down map """
    pos = Vec2(0, 0)
    trees = 0
    while pos.y + slope.y < slope_map.height:
        # Traverse down slope
        pos.x = pos.x + slope.x
        pos.y = pos.y + slope.y

        # Loop width if outside width bounds
        if pos.x >= slope_map.width:
            multiplier = math.ceil(pos.x / slope_map.width) or 1  # If 0 set to 1 to address zero index edge case
            pos.x = pos.x - (slope_map.width * multiplier)

        # Check if hitting a tree
        if slope_map.grid[pos.y][pos.x] == '#':
            trees += 1

    return trees


def calculate_trees_on_slopes(slope_map: Map, slopes: list[Vec2]) -> int:
    """ Return multiplied counts of trees on all slopes """
    ret = 1
    for slope in slopes:
        ret *= count_trees_slope(slope_map, slope)
    return ret


# Part 1
print(count_trees_slope(Map('input.txt'), Vec2(3, 1)))

# Part 2
print(calculate_trees_on_slopes(Map('input.txt'), [
    Vec2(1, 1),
    Vec2(3, 1),
    Vec2(5, 1),
    Vec2(7, 1),
    Vec2(1, 2)
]))

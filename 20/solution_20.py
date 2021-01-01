from operator import mul
from functools import reduce
import numpy as np
from scipy.signal import convolve2d
from math import sqrt


class Tile:
    up = None
    down = None
    left = None
    right = None
    oriented = False

    def __init__(self, id, data):
        self.id = id
        self.data = data

    def __repr__(self):
        return f'Tile: {self.id}'

    def rotate(self):
        self.data = np.rot90(self.data)

    def flip(self):
        self.data = self.data[::-1]

    def remove_borders(self):
        self.data = self.data[1:-1, 1:-1]

    def count_adjacent(self):
        return sum(bool(_) for _ in (self.up, self.down, self.left, self.right))

    def is_adjacent(self, other):
        s_top = self.data[0]
        s_bottom = self.data[-1]
        s_left = self.data[:, 0]
        s_right = self.data[:, -1]

        # Try all permutations of flipping and rotating
        for i in range(9):
            o_top = other.data[0]
            o_bottom = other.data[-1]
            o_left = other.data[:, 0]
            o_right = other.data[:, -1]

            if np.array_equal(s_top, o_bottom):
                self.up = other
                other.down = self
                self.oriented = other.oriented = True
                return True
            if np.array_equal(s_bottom, o_top):
                self.down = other
                other.up = self
                self.oriented = other.oriented = True
                return True
            if np.array_equal(s_left, o_right):
                self.left = other
                other.right = self
                self.oriented = other.oriented = True
                return True
            if np.array_equal(s_right, o_left):
                self.right = other
                other.left = self
                self.oriented = other.oriented = True
                return True

            if other.oriented:
                return False

            if i == 4:
                other.flip()
            else:
                other.rotate()


def load_tiles(inputfile):
    tiles = set()
    with open(inputfile, 'r') as infile:
        for raw_tile in infile.read().split('\n\n'):
            lines = raw_tile.splitlines()
            tile_id = int(lines[0].split()[-1][:-1])
            tiles.add(Tile(tile_id, np.array([list(int(c == '#') for c in r) for r in lines[1:]])))
    return tiles


def fit_tiles(tiles):
    start_tile = list(tiles)[0]
    queue = [start_tile]
    exhausted = set()
    while queue:
        tile = queue.pop()
        for other in tiles:
            if other == tile or other.id in exhausted:
                continue

            if tile.is_adjacent(other):
                queue.append(other)

        exhausted.add(tile.id)

    return tiles


def mul_corners(tiles):
    corner_tiles = [t for t in tiles if t.count_adjacent() == 2]
    return reduce(mul, [tile.id for tile in corner_tiles], 1)


def compile_image(tiles):
    top_left = None
    for tile in tiles:
        tile.remove_borders()
        if tile.up is None and tile.left is None:
            top_left = tile

    tile_width = int(sqrt(len(tiles)))
    data_width = len(top_left.data)
    output = np.zeros((data_width * tile_width, data_width * tile_width), np.uint8)

    row_start = top_left
    for row in range(tile_width):
        if row != 0:
            row_start = row_start.down

        current_tile = row_start
        for col in range(tile_width):
            if col != 0:
                current_tile = current_tile.right

            output[row * data_width: row * data_width + data_width,
            col * data_width: col * data_width + data_width] = current_tile.data

    return output


def count_sea_monsters(grid, monster_arr):
    # permutate through all rotations and flips
    for i in range(9):
        result_space = convolve2d(grid, monster_arr, mode='valid')
        result_space = result_space.astype(np.uint8)
        count = np.count_nonzero(result_space == monster_arr.sum())

        if count > 0:
            return count

        if i == 4:
            grid = grid[::-1]
        else:
            grid = np.rot90(grid)


def count_rough_waters(grid):
    monster = ['                  1 ',
               '1    11    11    111',
               ' 1  1  1  1  1  1   ']
    monster_arr = np.array([[int(char) if char != ' ' else 0 for char in line] for line in monster])
    monsters = count_sea_monsters(grid, monster_arr)

    return grid.sum() - monster_arr.sum() * monsters


tiles = fit_tiles(load_tiles('input.txt'))
# Part 1
print(mul_corners(tiles))

# Part 2
image = compile_image(tiles)
print(count_rough_waters(image))

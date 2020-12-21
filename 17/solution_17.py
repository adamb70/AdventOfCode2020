from itertools import product


def load_cubes(inputfile, dimensions=3):
    cubes = {}
    with open(inputfile, 'r') as infile:
        for i, row in enumerate(infile.read().splitlines()):
            for j, col in enumerate(row):
                if col == '#':
                    coords = [0] * dimensions
                    coords[0] = i
                    coords[1] = j
                    cubes[tuple(coords)] = 1
    return cubes


def get_neighbour_coords(coords, dimensions=3):
    """ Returns all surrounding block coords AND the block coords itself """
    for deltas in product([-1, 0, 1], repeat=dimensions):
        new_coords = []
        for i, val in enumerate(deltas):
            new_coords.append(coords[i] + val)
        yield tuple(new_coords)


def get_active_neighbours(grid, coords, dimensions=3):
    active_neighbours = 0

    for neighbour_coords in get_neighbour_coords(coords, dimensions):
        if neighbour_coords == coords:
            continue

        try:
            active_neighbours += grid[neighbour_coords]
        except KeyError:
            pass
    return active_neighbours


def expand_grid(active_keys, dimensions=3):
    """ Takes only grid coordinates where value == 1. Pads all outside cubes with 0. """
    new_grid = {}
    for key in active_keys:
        for neighbour_coords in get_neighbour_coords(key, dimensions):
            if neighbour_coords in active_keys:
                new_grid[neighbour_coords] = 1
            else:
                new_grid[neighbour_coords] = 0
    return new_grid


def run_cycle(grid, dimensions=3):
    new_grid = {}

    grid = expand_grid(set(grid.keys()), dimensions)
    for cube in grid:
        n = get_active_neighbours(grid, cube, dimensions)
        if grid[cube]:
            if n == 2 or n == 3:
                new_grid[cube] = 1
        else:
            if n == 3:
                new_grid[cube] = 1

    return new_grid


def run_cycles(grid, dimensions=3, count=1):
    for _ in range(count):
        grid = run_cycle(grid, dimensions)
    return len(grid)


# Part 1
dimensions = 3
grid = load_cubes('input.txt', dimensions)
print(run_cycles(grid, dimensions, count=6))

# Part 2
dimensions = 4
grid = load_cubes('input.txt', dimensions)
print(run_cycles(grid, dimensions, count=6))

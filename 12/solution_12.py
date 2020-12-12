def load_instructions(filepath):
    with open(filepath, 'r') as infile:
        return [(line[0], int(line[1:])) for line in infile.read().splitlines()]


def move_ship(instructions):
    pos = (0, 0)
    azimuth = 90
    headings = {
        0: (0, 1),
        90: (1, 0),
        180: (0, -1),
        270: (-1, 0),
    }

    for direction, magnitude in instructions:
        if direction == 'N':
            pos = (pos[0], pos[1] + magnitude)
        elif direction == 'E':
            pos = (pos[0] + magnitude, pos[1])
        elif direction == 'S':
            pos = (pos[0], pos[1] - magnitude)
        elif direction == 'W':
            pos = (pos[0] - magnitude, pos[1])

        elif direction == 'L':
            azimuth = (azimuth - magnitude) % 360
        elif direction == 'R':
            azimuth = (azimuth + magnitude) % 360

        elif direction == 'F':
            vec_x, vec_y = headings[azimuth]
            pos = (pos[0] + vec_x * magnitude, pos[1] + vec_y * magnitude)

    return abs(pos[0]) + abs(pos[1])


def move_waypoint(instructions):
    waypoint_pos = (10, 1)
    ship_pos = (0, 0)

    for direction, magnitude in instructions:
        if direction == 'N':
            waypoint_pos = (waypoint_pos[0], waypoint_pos[1] + magnitude)
        elif direction == 'E':
            waypoint_pos = (waypoint_pos[0] + magnitude, waypoint_pos[1])
        elif direction == 'S':
            waypoint_pos = (waypoint_pos[0], waypoint_pos[1] - magnitude)
        elif direction == 'W':
            waypoint_pos = (waypoint_pos[0] - magnitude, waypoint_pos[1])

        elif magnitude == 180 and direction in {'L', 'R'}:
            waypoint_pos = (-waypoint_pos[0], -waypoint_pos[1])
        elif (magnitude == 90 and direction == 'R') or (magnitude == 270 and direction == 'L'):
            waypoint_pos = (waypoint_pos[1], -waypoint_pos[0])
        elif (magnitude == 90 and direction == 'L') or (magnitude == 270 and direction == 'R'):
            waypoint_pos = (-waypoint_pos[1], waypoint_pos[0])

        elif direction == 'F':
            ship_pos = (ship_pos[0] + waypoint_pos[0] * magnitude, ship_pos[1] + waypoint_pos[1] * magnitude)

    return abs(ship_pos[0]) + abs(ship_pos[1])


instructions = load_instructions('input.txt')
# Part 1
print(move_ship(instructions))
# Part 2
print(move_waypoint(instructions))

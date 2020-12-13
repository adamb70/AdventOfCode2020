from math import lcm


def load_bus_times(filepath):
    with open(filepath, 'r') as infile:
        timestamp = int(infile.readline())
        bus_ids = infile.readline().split(',')

    return timestamp, bus_ids


def find_earliest_bus(bus_ids, timestamp):
    bus_ids = [int(b) for b in bus_ids if b != 'x']

    i = timestamp
    while True:
        for bus in bus_ids:
            if i % bus == 0:
                return (i - timestamp) * bus
        i += 1


def find_earliest_timestamp(bus_ids):
    # List buses and their time delta from the first bus
    buses = [(int(bus), delta) for delta, bus in enumerate(bus_ids) if bus != 'x']

    i = 1
    max_matches = 1
    bus, delta = max(buses, key=lambda x: x[0])  # Start with the largest bus value - can't be any smaller
    t = bus - delta  # Set initial time to first time the very first bus arrives
    increment_size = bus  # Start increments at the largest bus value
    while True:
        t += increment_size
        matches = set()  # Keep track of how many valid matches we have this run
        for bus, delta in buses:
            if int(t + delta) % bus != 0:
                # Not a valid match, jump ahead and try the next time
                i += increment_size
                break
            else:
                matches.add(bus)
                if len(matches) > max_matches:
                    max_matches = len(matches)
                    # We have found the next closest matching interval, set increment size to this interval
                    increment_size = lcm(*matches)
        else:
            # Matched all buses
            return t


timestamp, bus_ids = load_bus_times('input.txt')
# Part 1
print(find_earliest_bus(bus_ids, timestamp))
# Part 2
print(find_earliest_timestamp(bus_ids))

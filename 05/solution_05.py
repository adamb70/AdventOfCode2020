def get_seat_id(boarding_pass):
    rows = range(128)
    cols = range(8)

    for fb in boarding_pass[:7]:
        half_row_count = int((rows.stop - rows.start) / 2)
        if fb == 'F':
            rows = range(rows.start, rows.start + half_row_count)
        if fb == 'B':
            rows = range(rows.start + half_row_count, rows.stop)

    for lr in boarding_pass[7:]:
        half_col_count = int((cols.stop - cols.start) / 2)
        if lr == 'L':
            cols = range(cols.start, cols.start + half_col_count)
        if lr == 'R':
            cols = range(cols.start + half_col_count, cols.stop)

    return rows[0] * 8 + cols[0]


def get_highest_seat_id(passes):
    highest = 0

    for boarding_pass in passes:
        seat_id = get_seat_id(boarding_pass)
        if seat_id > highest:
            highest = seat_id

    return highest


def get_missing_seat_id(passes):
    seat_ids = set()
    for boarding_pass in passes:
        seat_ids.add(get_seat_id(boarding_pass))

    last_id = None
    for seat in seat_ids:
        if last_id and seat != last_id + 1:
            return seat - 1
        last_id = seat



with open('input.txt', 'r') as infile:
    boarding_passes = infile.read().splitlines()

# Part 1
print(get_highest_seat_id(boarding_passes))

# Part 2
print(get_missing_seat_id(boarding_passes))

from collections import Counter

def generate_weekly_list(start, end):
    start = start % 7
    end = end % 7
    if start <= end:
        return list(range(start, end + 1))
    else:
        return list(range(start, 7)) + list(range(0, end + 1))

def get_prioritized_shift(shifts):
    shift_counts = Counter(shifts)
    min_frequency = min(shift_counts.values())
    return [shift for shift in shifts if shift_counts[shift] == min_frequency]

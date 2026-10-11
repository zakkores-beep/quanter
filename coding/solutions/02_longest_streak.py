def longest_streak(days):
    s = set(days)
    best = 0
    for x in s:
        if x - 1 not in s:  # x starts a run
            y = x
            while y + 1 in s:
                y += 1
            best = max(best, y - x + 1)
    return best


def brute(days):
    best = 0
    for x in days:
        length = 0
        while x + length in days:  # list membership: O(n) each
            length += 1
        best = max(best, length)
    return best

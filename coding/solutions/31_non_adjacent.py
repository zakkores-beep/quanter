def max_non_adjacent(gains):
    take = skip = 0  # best total if today is taken / not taken
    for g in gains:
        take, skip = skip + g, max(take, skip)
    return max(take, skip)


def brute(gains):
    n = len(gains)
    best = 0
    for mask in range(1 << n):
        if mask & (mask >> 1) == 0:  # no two adjacent days
            best = max(best, sum(gains[i] for i in range(n) if mask >> i & 1))
    return best

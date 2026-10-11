def count_subarrays(pnl, k):
    seen = {0: 1}  # prefix sum -> how many times seen
    total = prefix = 0
    for x in pnl:
        prefix += x
        total += seen.get(prefix - k, 0)
        seen[prefix] = seen.get(prefix, 0) + 1
    return total


def brute(pnl, k):
    n = len(pnl)
    return sum(1 for i in range(n) for j in range(i, n) if sum(pnl[i:j + 1]) == k)

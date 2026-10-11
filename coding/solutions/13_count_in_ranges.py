def count_in_ranges(prices, queries):
    def first_at_least(x):
        lo, hi = 0, len(prices)
        while lo < hi:
            mid = (lo + hi) // 2
            if prices[mid] < x:
                lo = mid + 1
            else:
                hi = mid
        return lo

    return [first_at_least(hi + 1) - first_at_least(lo) for lo, hi in queries]


def brute(prices, queries):
    return [sum(1 for p in prices if lo <= p <= hi) for lo, hi in queries]

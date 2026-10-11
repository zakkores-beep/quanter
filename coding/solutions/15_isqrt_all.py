import math


def isqrt_all(nums):
    out = []
    for x in nums:
        lo, hi = 0, min(x, 10**9) + 1  # answer in [lo, hi)
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if mid * mid <= x:
                lo = mid
            else:
                hi = mid
        out.append(lo)
    return out


def brute(nums):
    """Count up for small x; for large x use the exact integer math.isqrt
    (an independent, exact implementation)."""
    out = []
    for x in nums:
        if x < 10**6:
            r = 0
            while (r + 1) * (r + 1) <= x:
                r += 1
            out.append(r)
        else:
            out.append(math.isqrt(x))
    return out

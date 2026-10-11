def days_needed(weights, cap):
    days, load = 1, 0
    for w in weights:
        if load + w > cap:
            days += 1
            load = 0
        load += w
    return days


def min_capacity(weights, days):
    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        if days_needed(weights, mid) <= days:
            hi = mid
        else:
            lo = mid + 1
    return lo


def brute(weights, days):
    cap = max(weights)
    while days_needed(weights, cap) > days:
        cap += 1
    return cap

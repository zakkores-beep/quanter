def edit_distance(a, b):
    prev = list(range(len(b) + 1))  # distance from a[:i] to b[:j]
    for i in range(1, len(a) + 1):
        cur = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1]
            else:
                cur[j] = 1 + min(prev[j - 1], prev[j], cur[j - 1])
        prev = cur
    return prev[-1]


def brute(a, b):
    """Plain recursion over all edit choices, no memo (exponential)."""
    if not a:
        return len(b)
    if not b:
        return len(a)
    options = [1 + brute(a[1:], b), 1 + brute(a, b[1:]), (a[0] != b[0]) + brute(a[1:], b[1:])]
    return min(options)

from itertools import combinations


def common_subsequence(a, b):
    prev = [0] * (len(b) + 1)
    for ch in a:
        cur = [0]
        for j in range(len(b)):
            cur.append(prev[j] + 1 if ch == b[j] else max(prev[j + 1], cur[j]))
        prev = cur
    return prev[-1]


def brute(a, b):
    """Try subsequences of `a`, longest first, and test each against `b`."""
    def is_subseq(s, t):
        it = iter(t)
        return all(ch in it for ch in s)

    for r in range(len(a), 0, -1):
        for combo in combinations(a, r):
            if is_subseq(combo, b):
                return r
    return 0

def longest_unique(s):
    last = {}
    start = best = 0
    for i, ch in enumerate(s):
        if last.get(ch, -1) >= start:
            start = last[ch] + 1
        last[ch] = i
        best = max(best, i - start + 1)
    return best


def brute(s):
    n = len(s)
    best = 0
    for i in range(n):
        for j in range(i + 1, n + 1):
            if len(set(s[i:j])) == j - i:
                best = max(best, j - i)
    return best

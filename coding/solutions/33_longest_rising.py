from bisect import bisect_left
from itertools import combinations


def longest_rising(prices):
    tails = []  # tails[L] = smallest tail of a rising subsequence of length L + 1
    for p in prices:
        i = bisect_left(tails, p)
        if i == len(tails):
            tails.append(p)
        else:
            tails[i] = p
    return len(tails)


def brute(prices):
    for r in range(len(prices), 0, -1):
        for combo in combinations(prices, r):
            if all(a < b for a, b in zip(combo, combo[1:])):
                return r
    return 0

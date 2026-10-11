import heapq
from collections import Counter


def top_k_tickers(trades, k):
    counts = Counter(trades)
    return [t for _, t in heapq.nsmallest(k, ((-c, t) for t, c in counts.items()))]


def brute(trades, k):
    distinct = set(trades)
    return sorted(distinct, key=lambda t: (-trades.count(t), t))[:k]

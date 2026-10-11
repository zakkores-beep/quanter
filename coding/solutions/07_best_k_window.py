def best_window(pnl, k):
    cur = sum(pnl[:k])
    best = cur
    for i in range(k, len(pnl)):
        cur += pnl[i] - pnl[i - k]
        best = max(best, cur)
    return best


def brute(pnl, k):
    return max(sum(pnl[i:i + k]) for i in range(len(pnl) - k + 1))

def count_pairs(prices, target):
    seen = {}
    total = 0
    for p in prices:
        total += seen.get(target - p, 0)
        seen[p] = seen.get(p, 0) + 1
    return total


def brute(prices, target):
    n = len(prices)
    return sum(1 for i in range(n) for j in range(i + 1, n) if prices[i] + prices[j] == target)

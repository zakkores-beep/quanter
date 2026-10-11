from collections import deque


def min_coins(lots, amount):
    inf = float("inf")
    dp = [0] + [inf] * amount
    for a in range(1, amount + 1):
        for c in lots:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return -1 if dp[amount] == inf else dp[amount]


def brute(lots, amount):
    """Breadth-first search over totals: the first time we hit `amount` uses the fewest lots."""
    dist = {0: 0}
    queue = deque([0])
    while queue:
        x = queue.popleft()
        if x == amount:
            return dist[x]
        for c in lots:
            y = x + c
            if y <= amount and y not in dist:
                dist[y] = dist[x] + 1
                queue.append(y)
    return -1

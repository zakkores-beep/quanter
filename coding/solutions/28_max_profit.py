def max_profit(prices):
    return sum(max(0, b - a) for a, b in zip(prices, prices[1:]))


def brute(prices):
    """Try every buy/sell/hold decision (exponential)."""
    def best(i, holding):
        if i == len(prices):
            return 0
        skip = best(i + 1, holding)
        if holding:
            return max(skip, prices[i] + best(i + 1, False))
        return max(skip, -prices[i] + best(i + 1, True))

    return best(0, False)

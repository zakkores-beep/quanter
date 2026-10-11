from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 28
TITLE = "Unlimited Round Trips"
LEVEL = "easy"
TOPIC = "greedy"
FUNC = "max_profit"
SIGNATURE = "def max_profit(prices: list[int]) -> int:"
STATEMENT = """
`prices[i]` is a stock's price on day `i`. You may buy and sell as many
times as you like, but you can hold at most one share at a time (sell
before buying again). Buying and selling happen at that day's price.
Return the maximum total profit (0 if you never trade).
"""
CONSTRAINTS = """
- `1 <= len(prices) <= 2 * 10**5`
- `0 <= prices[i] <= 10**4`
"""
EXAMPLES = [dict(prices=[1, 5, 3, 6, 4]), dict(prices=[5, 4, 3])]


def edge_cases():
    return [dict(prices=[5]), dict(prices=[1, 2, 3, 4, 5]), dict(prices=[3, 3, 3]), dict(prices=[0, 10**4, 0, 10**4]),
            dict(prices=[2, 1, 2, 1, 2])]


def random_case(rng):
    return dict(prices=[rng.randint(0, 10) for _ in range(rng.randint(1, 12))])


def perf_case(rng):
    return dict(prices=[rng.randint(0, 10**4) for _ in range(200000)])


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return size(c['prices'], 1, 2 * 10**5) and ints(c['prices'], 0, 10**4)

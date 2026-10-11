from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 11
TITLE = "Days Until a Higher Price"
LEVEL = "medium"
TOPIC = "stack"
FUNC = "days_until_higher"
SIGNATURE = "def days_until_higher(prices: list[int]) -> list[int]:"
STATEMENT = """
For each day `i`, return how many days you must wait until a **strictly
higher** price than `prices[i]`. Use 0 if no later day has a higher price.
"""
CONSTRAINTS = """
- `1 <= len(prices) <= 2 * 10**5`
- `1 <= prices[i] <= 10**6`
"""
EXAMPLES = [dict(prices=[73, 71, 75, 70, 76, 72]), dict(prices=[3, 3, 3])]


def edge_cases():
    return [dict(prices=[5]), dict(prices=[1, 2, 3]), dict(prices=[3, 2, 1]), dict(prices=[2, 1, 2, 5]),
            dict(prices=[10**6, 1, 10**6]), dict(prices=[1, 5, 1, 5, 6])]


def random_case(rng):
    n = rng.randint(1, 12)
    return dict(prices=[rng.randint(1, 6) for _ in range(n)])


def perf_case(rng):
    down = [10**6 - i * 5 - rng.randint(0, 4) for i in range(150000)]
    return dict(prices=down + [rng.randint(1, 10**6) for _ in range(50000)])


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return size(c['prices'], 1, 2 * 10**5) and ints(c['prices'], 1, 10**6)
